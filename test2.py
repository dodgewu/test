import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
async def test():
    snmpEngine = SnmpEngine()
    g = get_cmd(
                snmpEngine,
                CommunityData('public'),
                # await UdpTransportTarget.create(('172.16.160.32', 161)),
                await UdpTransportTarget.create(('demo.pysnmp.com', 161)),
                ContextData(),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0))
                )
    
    print(g)


    errorIndication, errorStatus, errorIndex, varBinds = await g
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
asyncio.run(test())