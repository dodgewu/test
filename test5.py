import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement,dut


async def test(start_index,imple):
    for i in range(start_index,len(imple)+1):
        oid_list=['1.3.6.1.4.1.35604.2.4.1.7.1.2.1.8','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.2','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.3','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.4','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.5','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.6','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.7','1.3.6.1.4.1.35604.2.4.1.7.1.2.1.8']
        oid_index=[]
        for i in range(0,len(oid_list)):
            tmp=oid_list[i]+'.'+str(start_index)
            oid_index.append(tmp)
        for i in oid_index:
            print(i)
        start_index+=1
        return
    snmpEngine = SnmpEngine()
    # 依序排需要set 的oid
    
    
    ll = await set_cmd(
        snmpEngine,
        CommunityData("public", mpModel=1),
        await UdpTransportTarget.create(("172.16.160.26", 161)),
        ContextData(),
        ObjectType(ObjectIdentity("1.3.6.1.4.1.35604.2.4.1.7.1.2.1.8.2"),Integer32(5)),
    )
    errorIndication, errorStatus, errorIndex, varBinds =  ll



    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print(
            "{} at {}".format(
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
            )
        )
    else:
        for varBind in varBinds:
            print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()

async def main():
    implem=[(8200,8200,8250,8260,'udp'),(8310,8320,8400,8400,'udp'),(8500,8550,8560,'udp')]
    await test(3,imple=implem)
if __name__=="__main__":
    asyncio.run(main())