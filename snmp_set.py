
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import reboot


async def my_set():
    ip=input("Please input an DUT's ip to set the value!!\n")
    oid="1.3.6.1.4.1.35604.2.3.14.6.0"
    ass_value=input(f"Please enter the value to assgined the oid\n({oid})\n")
    snmpEngine=SnmpEngine() 
    result= set_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    # 不知道有沒有順序問題，其result 結果是否也照順序???
                    ObjectType(ObjectIdentity(oid),Integer(ass_value)),
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
            print(f"{oid}:\n = {varBind}")
    snmpEngine.close_dispatcher()
asyncio.run(my_set())