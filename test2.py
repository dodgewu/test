import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from test3 import store_statement

# This program can able to write the get response write into txt file 
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
    
    await store_statement(g)
    snmpEngine.close_dispatcher()
asyncio.run(test())