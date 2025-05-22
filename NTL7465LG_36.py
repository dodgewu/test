import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement,telnet_connection,telnet_operation,snmp_operation

async def test(dut):
    """此funciotn測試NTL7465LG-36，
    1. 主要有兩個測試:
        (1) 在CMTS上看DUT的BPI要上線。
        (2) 在MIBS上看BPI要上線(docsBpi2CmPrivacyEnable)
    2. Argument 為DUT's instance。
    3. 執行步驟:
        (1) 建立logger instance
        (2) 連線CMTS去看DUT的BPI情況
        (3) 用snmp_get(SNMP)去看DUT的BPI情況    
        (4) 比對兩者的結果
        (5) 返回
    """
    try:
        test_case='NTL7465LG_36'
        # Step1
        my_logger=error_statement.SNMPResultLogger(dut,test_case)
        my_logger.init_folder()
        # Step2
        my_conn= telnet_connection.tel_connection(dut)
        result1=await telnet_operation.bpi(my_conn,dut,my_logger)
        # Step3
        my_snmp=snmp_operation.MySnmp(dut,test_case)
        result2=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.126.1.1.1.1.1.2')
        # Step4
        await chk_bpi(result1,result2)
        return
    
    except Exception as e:
        print(e)
async def chk_bpi(result1:bool,result2:str):
    """此function用以判斷bpi是否開啟，bool type 為CMTS，str type 則為SNMP result。"""
    if result1 and (result2==1):
        print("DUT provisioning with BPI in CMTS.(Passed!!)")
        return
    print("DUT provisioning with BPI in CMTS.(Failed!!)")

if __name__=="__main__":
    asyncio.run(test())