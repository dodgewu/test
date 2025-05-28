import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import reboot,error_statement,dut


class MySnmp():
    def __init__(self,dut,test_case,community='private',snmp_ver=1):
        self.oid=None
        self.base_type=None
        self.value=None
        self.community=community
        self.snmp_ver=snmp_ver
        self.test_case=test_case
        self.dut=dut 
        self.ip=dut.ip
    
    def set_oid(self,oid):
        """This method is used to set the OID of MIBs that you want to set."""
        self.oid=oid
    
    async def set_base_type(self,oid):
        """This method is used to set the base type of MIBs that you want to set."""
        self.base_type= await self.get_base_type(oid,self.dut)
    
    def set_value(self,value):
        """This method is used to set the value of MIBs that you want to set."""    
        self.value=value
        self.type_transfor(value,self.base_type)

    async def my_snmp_set(self,logger,oid,value):
        """This method assists users in setting MIB (Management Information Base) values using the snmpset command, 
        allowing configurations based on the base types defined within the MIB."""
        try:
            # 設定SNMP的OID
            self.set_oid(oid)
            await self.set_base_type(oid)
            self.set_value(value)
            snmpEngine=SnmpEngine() 
            result= await set_cmd(snmpEngine,
                            CommunityData(self.community,mpModel=self.snmp_ver),
                            await UdpTransportTarget.create((f'{self.dut.ip}',161)),
                            ContextData(),
                            ObjectType(ObjectIdentity(self.oid),self.value),
                            )
            # 寫入資訊
            logger.store_result(self.dut,result)
            snmpEngine.close_dispatcher()
        except Exception as e:
            print(f"There is an error occured when setting the value of MIBs you assigned.{e}")

    def type_transfor(self,value,base_type):
        """This method can transform the base type of value."""
        try:
            match base_type:
                case 'Integer32':
                    self.value = Integer32(value)
                case 'Gauge32':
                    self.value = Gauge32(value)
                case 'OctetString':
                    self.value = OctetString(value)
                case 'Counter32':
                    self.value = Counter32(value)
                case 'Counter64':
                    self.value = Counter64(value)
                case 'IpAddress':
                    self.value = IpAddress(value)
                case 'Opaque':
                    self.value = Opaque(value)
                case 'TimeTicks':
                    self.value = TimeTicks(value)
                case 'ObjectIdentifier':
                    self.value = ObjectIdentifier (value)
        except Exception as e :
            print(f"There is an error occured when transform the base type of value you assigned.{e}")
    
    async def my_snmp_get(self,logger,oid):
            """you can get an value of MIB,it will return a ObjectType for User to analysis the result of snmpget.
            """
            snmpEngine = SnmpEngine()
            result = await get_cmd(
                        snmpEngine,
                        CommunityData(self.community,mpModel=self.snmp_ver),
                        await UdpTransportTarget.create((str(self.ip), 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid)),
                        )
            a,b,c,d=result
            tmp=None
            for i in d:
                self.result=type(i[1])
                tmp= i[1].prettyPrint()

            # 存入log檔
            logger.store_result(self.dut,result)
            snmpEngine.close_dispatcher()
            
            # 回傳 str type 的結果
            return tmp

    async def get_base_type(self,oid,dut)-> str: 
        """In this method, you can get one base type of MIB(OID). 
        The base type will helpful when you are using my_snmp_get() to transform the type of assigned value. """
        snmpengine=SnmpEngine()
        result=get_cmd(
            snmpengine,
            CommunityData(self.community,mpModel=self.snmp_ver),
            await UdpTransportTarget.create((dut.ip,161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid))
        )
        a,b,c,d= await result
        tmp=''
        for tmp_oid,tmp_value in d:
            tmp= str(type(tmp_value).__name__)
        snmpengine.close_dispatcher()
        self.base_type=type(tmp)
        return tmp

    async def my_snmp_walk(self,logger,oid,end_oid):
        """此function 可以跑一整個table e.g.ifTable。
            需自行設定結束OID。
        """
        try:
            snmpEngine = SnmpEngine()
            # walk_cmd是多個get_next組成，回傳generator
            result=  walk_cmd(
                            snmpEngine,
                            CommunityData(self.community,mpModel=self.snmp_ver),
                            await UdpTransportTarget.create((self.ip, 161)),
                            ContextData(),
                            ObjectType(ObjectIdentity(oid)),
                            lexicographicMode=False
                            )
            #generate generator 的值
            g = [item async for item in result]

            # 設定結束的OID
            end=''
            # 設定i為0，因為g是list，所以可以用index來取值
            i=0
            store_into_log=''
            while end!=end_oid and i < len(g):    
                for d in g[i][3]:
                        end = d[0]
                        tmp=f"{d[0]}={d[1].prettyPrint()}"
                        store_into_log+=f"{tmp}\n"
                        i+= 1
             # 存入log檔
            logger.store_result(self.dut,store_into_log)
            snmpEngine.close_dispatcher()
            return store_into_log
        except Exception as e:
            print(f"There is an error occured when walking the table of MIBs you assigned.{e}")

if __name__=='__main__':
    my_dut=dut.Dut(ip='172.16.42.14',cmts='172.16.1.9',mac='f8fb',fw='Test',wifi_24_ver=None,wifi_55_ver=None)
    # test36= NTL7465LG_36.test(my_dut)
    # await test36
    my_get=MySnmp(my_dut)
    asyncio.run(my_get.my_snmp_set())