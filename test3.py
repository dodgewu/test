import os,logging,asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime

async def test():
    """For CD8021 regression test"""
    snmpengine=SnmpEngine()
    myl=['coex-fivecpeonly','coex-readtrap','coex-trapsonly','coex-allcpe','coex-subnetcpe','coex-diagIp','coex-diagIpSubnet']
    for i in myl:
        ipv4='172.16.160.24'
        ipv6='2002:db50:fa13:160:ec93:5717:d6d5:1331'
        oid='1.3.6.1.2.1.1.6.0'

        result1= await set_cmd(snmpengine,
                        CommunityData(i,mpModel=0),
                        await UdpTransportTarget.create((f'{ipv4}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid),OctetString('test'))
                        )
        result2= await set_cmd(snmpengine,
                        CommunityData(i,mpModel=0),
                        await Udp6TransportTarget.create((f'{ipv6}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid),OctetString('test'))
                        )
        result3= await get_cmd(snmpengine,
                        CommunityData(i,mpModel=0),
                        await UdpTransportTarget.create((f'{ipv4}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                        )
        result4= await get_cmd(snmpengine,
                        CommunityData(i,mpModel=0),
                        await Udp6TransportTarget.create((f'{ipv6}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                        )

        print(f"{i}:\nset:ipv4={result1} \nipv6={result2}\n")
        print(f"--------------------------------------------\n")
        print(f"get:ipv4={result3} \nipv6={result4}\n")
        print(f"--------------------------------------------\n")
        print(f"--------------------------------------------\n")
asyncio.run(test())