import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement,dut,snmp_operation,error_check


# *******************************************************
# *****此code已被棄用，現用snmp_operation 來執行 get,set...操作。
# *****2025/05/22
# *******************************************************

class MyGet():
    def __init__(self,dut,oid="1.3.6.1.4.1.35604.2.2.1.31.0",community='private',snmp_ver=1):
        self.dut=dut
        self.oid=oid
        self.result=None
        self.base_type=None
        self.community=community
        # value= 0(v1),1(v2)
        self.snmp_ver=snmp_ver

    async def my_snmp_get(self,logger):
        """you can get an value of MIB,it will return a ObjectType for User to analysis the result of snmpget.
        """
        snmpEngine = SnmpEngine()
        result = await get_cmd(
                    snmpEngine,
                    CommunityData(self.community,mpModel=self.snmp_ver),
                    await UdpTransportTarget.create((str(self.dut.ip), 161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(self.oid)),
                    )
        a,b,c,d=result
        tmp=''
        for i in d:
            self.result=type(i[1])
            tmp=i[1]
        # 存入log檔
        logger.store_result(self.dut,result)
        snmpEngine.close_dispatcher()
        return tmp
    
    async def get_base_type(self,oid,dut)-> str: 
        """In this method, you can get one base type of MIB(OID). 
        The base type will helpful when you are using my_snmp_get() to transform the type of assigned value. """
        snmpengine=SnmpEngine()
        result=get_cmd(
            snmpengine,
            CommunityData(dut.community,mpModel=dut.snmp_ver),
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
    
    async def chk_value(self,value):
        tmp=self.base_type
        print(f"value:{tmp}\ntype:{type(tmp)}")


    # not finished, tried to walk multi-MIBs
    async def my_walk():
        # ip=str(input("please enter an ip to walk the mibs.\n"))
        ip='172.16.160.32'
        oid='1.3.6.1.4.1.35604.2.3.1.1.1.1.1.1'
        snmpEngine=SnmpEngine()
        w=walk_cmd(
            snmpEngine,
            CommunityData('private'),
            await UdpTransportTarget.create((ip,161)),
            ContextData(),
            ObjectType(ObjectIdentity(oid)),
            # 設定walk(getnext)個數
            maxRows=2017
        )
        async for walk_result in w:
            my_snmp_get_name="NTL7465LG-8299"
            statement1=error_statement.SNMPResultLogger("pheonix",my_snmp_get_name)
            statement1.init_folder()
            statement1.store_result(my_snmp_get_name,walk_result)
            # if errorIndication:
            #     print(errorIndication)

            # elif errorStatus:
            #     print(
            #         "{} at {}".format(
            #             errorStatus.prettyPrint(),
            #             errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            #         )
            #     )
            # else:
            #     for varBind in varBinds:
            #         print("{}\n------------------------------------------------------------------".format(varBind))    

        snmpEngine.close_dispatcher()

if __name__=='__main__':
    my_dut=dut.Dut(ip='172.16.160.24',cmts='172.16.1.6',mac='f8fb',fw='Test',wifi_24_ver=None,wifi_55_ver=None)
    # test36= NTL7465LG_36.test(my_dut)
    # await test36
    my_get=MyGet(my_dut)
    asyncio.run(my_get.get_base_type())
    asyncio.run(my_get.chk_value(22))