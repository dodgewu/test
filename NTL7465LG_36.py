import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from  error_check import check
import error_statement,telnet_connection,dut

async def test(dut):
    """此funciotn測試NTL7465LG-36，主要有兩個測試，1. 在CMTS上看DUT的BPI要上線。2. 在MIBS上看BPI要上線(docsBpi2CmPrivacyEnable)，
    Argument 為DUT's instance"""
    try:
        # step1. 看CMTS 上 BPI
        await telnet_connection.telnet_conn(dut.cmts,dut.mac,'bpi')

        # step2. MIBS 看BPI
        snmpEngine=SnmpEngine()
        result=await get_cmd(SnmpEngine(),CommunityData('private',mpModel=1), 
                        await UdpTransportTarget.create((f'{dut.ip}',161)),
                        ContextData(),
                        # docsBpi2CmPrivacyEnable
                        ObjectType(ObjectIdentity('1.3.6.1.2.1.126.1.1.1.1.1.2'))
        )
        # 將 result 寫進file 中, file path=> D:\Data\pysnmp\FWNAME\TESTNAME\CURRENTDAY.txt
        statement1=error_statement.SNMPResultLogger(dut.fw,dut.test_case)
        statement1.init_folder()
        bpi_res=statement1.store_result(dut.test_case,result)
        # 分析結果
        errorIndication, errorStatus, errorIndex, varBinds = result
        ##ObjectType分解
        x=varBinds[0].prettyPrint()

        if x[len(x)-1]!='1':
            print("BPI isn't enabled on MIBs (Failed!)")
            return 
        print("BPI is enabled on MIBs (Successful!)")
        snmpEngine.close_dispatcher()
    except Exception as e:
        print(e)
if __name__=="__main__":
    asyncio.run(test())