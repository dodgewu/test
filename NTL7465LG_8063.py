import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement
# from  error_check import check
import snmp_get



# NOT REWRITE　Yet
# This program can able to write the get response and write into a text file 

def mac_compare(__varBinds):
    """判斷index 2,12,32,92 MAC address 開頭為 00(default) 或 cbn(非00)"""
    my_list=[]
    for i in __varBinds:
        my_list.append(str(i))
    print(my_list[1][33:37])
    for j in my_list:
        if j[33:35]!=00:
            return True
        return False

# main program
async def test(dut):
    my_get=snmp_get.MyGet(dut,oid='1.3.6.1.2.1.2.2.1.6.2.0')
    my_result=await my_get.my_snmp_get()
    print(f"{my_result}type{type(my_result)}")
    # snmpEngine = SnmpEngine()
    # my_result = await get_cmd(
    #             snmpEngine,
    #             CommunityData('private'),
    #             await UdpTransportTarget.create((f'{ip}', 161)),
    #             ContextData(),
    #             ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.6.2")),
    #             ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.6.16")),
    #             ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.6.32")),
    #             ObjectType(ObjectIdentity("1.3.6.1.2.1.2.2.1.6.92"))
    #             )
    # errorIndication, errorStatus, errorIndex, varBinds =  my_result
    # error_check_result= check(my_result)
    # mac_check=False
    # if error_check_result:
    #     mac_check=mac_compare(varBinds)
    #     store_statement(my_result)
    # if mac_check:
    #     print(f"The MAC addresses are assigned by cbn. \n")
    #     for i in varBinds:
    #         print(i)
    # else:
    #     print("[Hint] The MAC address on index 2,12,32,92 are Default MAC address")
    
    # snmpEngine.close_dispatcher()


# if __name__=="__main__":
#     ip="172.16.42.157"
    # asyncio.run(test_8063(ip))


