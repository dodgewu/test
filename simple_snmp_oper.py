
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import ipaddress


async def my_simple_oper():
    oper='3'
    ip='172.16.160.24'
    oid='1.3.6.1.2.1.10.127.1.1.4'
    if oper == None or ip == None:
        oper=input("Please input the operation you want to do(1:set;2:get;3:walk table)\n")
        ip=input("Please input an DUT's ip\n")
        oid=input("Please input the OID you want to operate\n")
    if ipaddress.ip_address(ip).version == 6:
        ipversion=6
    elif ipaddress.ip_address(ip).version == 4:
        ipversion=4
    else:
        return "IP format wrong"
    
    if oper=='1':
        value=input("Please input the value you want to set\n")
    snmpEngine=SnmpEngine() 
    if oper=='1':   
        if ipversion==4:
            # IPv4
            result= set_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    # 不知道有沒有順序問題，其result 結果是否也照順序???
                    ObjectType(ObjectIdentity(oid),Integer(value))
                    
                    )
        else:
            # IPv6
            result= set_cmd(snmpEngine,
                        CommunityData('private',mpModel=1),
                        await Udp6TransportTarget.create((f'{ip}',161)),
                        ContextData(),
                        # 不知道有沒有順序問題，其result 結果是否也照順序???
                        ObjectType(ObjectIdentity(oid),OctetString(value))
                        
                        )
    elif oper=='2':
        if ipversion==4:
            # IPv4
            result= get_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid))
                    )
        else:
            # IPv6
            result= get_cmd(snmpEngine,
                        CommunityData('private',mpModel=1),
                        await Udp6TransportTarget.create((f'{ip}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid))
                        )
    elif oper=='3':
        if ipversion==4:
            result= next_cmd(snmpEngine,
                        CommunityData('private',mpModel=1),
                        await UdpTransportTarget.create((f'{ip}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid)),
                        lexicographicalMode=False
                        )
        else:
            result= next_cmd(snmpEngine,
                        CommunityData('private',mpModel=1),
                        await Udp6TransportTarget.create((f'{ip}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity(oid)),
                        lexicographicalMode=True
                        )

    
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
            print(f"{varBind[0]} = {varBind[1]}")
    snmpEngine.close_dispatcher()

asyncio.run(my_simple_oper())