
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import reboot


async def my_reset():
    ip=input("Please input an DUT's ip to reset it!!\n")
    my_warning=input("Are you sure you wanna reset it to default?(y/n)\n")
    if my_warning!='y':
        print("Reset to default stopped!!!")
        return 
    reset_oid="1.3.6.1.4.1.35604.2.2.1.3.0"
    reboot_oid="1.3.6.1.2.1.69.1.1.3.0"
    snmpEngine=SnmpEngine() 
    result= set_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    # 不知道有沒有順序問題，其result 結果是否也照順序???
                    ObjectType(ObjectIdentity(reset_oid),Integer(1)),
                    ObjectType(ObjectIdentity(reboot_oid),Integer(1))
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
            print(f"reset to default:\n = {varBind}")
    snmpEngine.close_dispatcher()
asyncio.run(my_reset())