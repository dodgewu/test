
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# 此程式用來執行 重新開機(docsDevResetNow)

async def my_set():
    ip=input("Please input an DUT's ip to restart it.")
    snmpEngine=SnmpEngine() 
    result= set_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    ObjectType(ObjectIdentity("1.3.6.1.2.1.69.1.1.3.0"),Integer(1)))
    # result= set_cmd(snmpEngine,CommunityData('private',mpModel=1),await UdpTransportTarget.create(('172.16.42.157',161)),ContextData(),ObjectType(ObjectIdentity("1.3.6.1.2.1.69.1.1.3.0"),Integer(1)))
    
    errorIndication,    errorStatus,  errorIndex, varBinds = await result

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
               
asyncio.run(my_set())