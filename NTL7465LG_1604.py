import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement,telnet_connection,snmp_operation,re

async def test(dut):
    """此funciotn測試NTL7465LG-1604，主要測試wifi version 是否正確，若released note沒有提及，則跟之前一樣。
        流程:利用MIBs下 console(ARM)指令，再get MIBs的回傳值。
    """
    try:
        # 宣告test_name
        test_case='NTL7465LG_1604'
        # 宣告logger
        my_logger=error_statement.SNMPResultLogger(dut,test_case)
        my_logger.init_folder()
        # 宣告 empty list 
        wifi_ver=[]
        
        # Step1. 輸入Console指令找24Gwifi version
        my_snmp1=snmp_operation.MySnmp(dut,test_case)
        await my_snmp1.my_snmp_set(logger=my_logger,oid='1.3.6.1.4.1.35604.2.3.103.0',value="cat /etc/Wireless/CL242/env.sh")
        
        # Step2. 獲取24Gwifi version
        my_snmp2=snmp_operation.MySnmp(dut,test_case)
        tmp1=await my_snmp2.my_snmp_get(my_logger,'1.3.6.1.4.1.35604.2.3.104.0')

        # Step3. 輸入Console指令找55Gwifi version
        await my_snmp1.my_snmp_set(my_logger,'1.3.6.1.4.1.35604.2.3.103.0',"cat /etc/Wireless/CL242/env.sh")

        # Step4. 獲取55Gwifi version
        tmp2=await my_snmp2.my_snmp_get(my_logger,'1.3.6.1.4.1.35604.2.3.104.0')

        # Step5. 對結果進行判斷
        wifi_ver.append(('2.4g',tmp1))
        wifi_ver.append(('55g',tmp2))
        wifi_ver_chk(wifi_ver,dut)
        return
    
    except Exception as e:
        print(e)
def wifi_ver_chk(a:list,b):
    """This function can verify the Wi-Fi version is the lastest or not.
    The lastest Wi-Fi version need user to write in manually"""
    try:
        # 先 check 24G
        tmp=str(a[0][1])
        if tmp.find(str(b.wifi_24_ver))!=-1:
            print("Wi-Fi versoin of 2.4G is expected.(Passed!!)\n")
        else:
            print("Wi-Fi versoin of 2.4G isn't expected.(Failed!!)\n")
        # 再check 55G 
        tmp=str(a[1][1])
        if tmp.find(str(b.wifi_55_ver))!=-1:
            print("Wi-Fi versoin of 55G is expected.(Passed!!)\n")
        else:
            print("Wi-Fi versoin of 55G isn't expected.(Failed!!)\n")
        print(f"------------------------------------")
        return 
    except Exception as e:
        print(f"There is somethings wrong when WiFi comparasion is processing.[ERROR]{e}")
if __name__=="__main__":
    asyncio.run(test())