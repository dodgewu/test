import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from  error_check import check
import error_statement
# This program can able to write the get response and write into a text file 

test_name='NTL7465LG_860'
#snmpwalk (1.3.6.1.2.1.69.1.3.5.0)

async def docsDevSwCurrentVers(ip):
    try:
        snmpEngine=SnmpEngine()
        result=await get_cmd(SnmpEngine(),CommunityData('public',mpModel=1), 
                        await UdpTransportTarget.create((f'{ip}',161)),
                        ContextData(),
                        ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.5.0'))
        )
        # 將 result 寫進file 中, file path=> D:\Data\pysnmp\FWNAME\TESTNAME\CURRENTDAY.txt
        statement1=error_statement.SNMPResultLogger('20280418_6.15.35eng-1-SH(NA)',"NTL7465LG_860")
        statement1.init_folder(test_name)
        statement1.store_result(test_name,result)
        snmpEngine.close_dispatcher()
    except Exception as e:
        print(e)
    

# main program
async def test_860(ip):
    test1 = asyncio.create_task(docsDevSwCurrentVers(ip))
    await test1
asyncio.run(test_860('172.16.42.199'))
# if __name__=="__main__":
#     ip="172.16.42.157"
    # asyncio.run(test_8063(ip))


