
import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import test

# 此程式用來執行 重新開機(docsDevResetNow)
# 獨立的程式

async def my_set(ip):
    oid="1.3.6.1.2.1.69.1.1.3.0"
    snmpEngine=SnmpEngine() 
    result= set_cmd(snmpEngine,
                    CommunityData('private',mpModel=1),
                    await UdpTransportTarget.create((f'{ip}',161)),
                    ContextData(),
                    ObjectType(ObjectIdentity(oid),Integer(1)))
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
            print(f"{oid} = {varBind}")
    snmpEngine.close_dispatcher()

async def my_test():
    print("1")
    await asyncio.sleep(5)
    print("2")
    await asyncio.sleep(5)      
if __name__=="__main__":
    # oper=input("Please input the operation you want to do:(reboot/nor/mac) ")
    # my_list=['172.16.150.34','172.16.150.37','172.16.150.41','172.16.150.46','172.16.150.36','172.16.150.33','172.16.150.19']
    # #reboot
    # if oper=="reboot":
    #     for i in my_list:
    #         print(f"Rebooting {i}...")
    #         asyncio.run(my_set(i))
    # # 升級
    # if oper=='nor' or oper=='mac':
    #     print(f"Upgrading to {oper}...")
    #     asyncio.run(test.bulk_upgrade_0529(my_list,oper))
    while True:
        asyncio.run(my_test())
    



