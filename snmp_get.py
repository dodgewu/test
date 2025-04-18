import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
async def test():
    snmpEngine = SnmpEngine()
    g = get_cmd(
                snmpEngine,
                CommunityData('private'),
                # await UdpTransportTarget.create(('172.16.160.32', 161)),
                await UdpTransportTarget.create(('172.16.42.199', 161)),
                ContextData(),
                ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity("1.3.6.1.2.1.69.1.3.5.0"))
                )
    
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
            print("{}\n------------------------------------------------------------------".format(varBind))
            # print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()
asyncio.run(test())