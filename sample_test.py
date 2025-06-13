import asyncio,dut,error_statement,snmp_operation,os
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
# import pandas,openpyxl

async def sample_test(dut,my_tuple):
    # CD8021 submission test
    """This function is used to test the CD8021 submission."""

    # 1. 獲取ehternet mac
    # 2. 獲取hfc mac
    # 3. sysDesrc check 
    # 4. docsDevSwCurrentVers check 
    # 5. Completeness of ifTable
    # 6. get SN number 
    try:
        index,mac,ip=my_tuple
        docsis='D31'
        d_ver='MAC14'
        test_case=f'CD8021_{index}_{mac}'
        my_logger=error_statement.SNMPResultLogger(dut,test_case)
        my_logger.init_folder()
        my_snmp=snmp_operation.MySnmp(dut,test_case)
        # 1. 獲取ehternet mac
        result1=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.2.2.1.6.1')
        if result1 == '':
            print("Ethernet MAC (Failed!!)")
        else:
            print(f"Ethernet MAC: {result1}(Passed!!)")
        # 2. 獲取hfc mac
        result2=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.2.2.1.6.2')
        if result2 == '':
            print("HFC MAC (Failed!!)")
        else:
            print(f"HFC MAC: {result2}(Passed!!)")
        # 3. sysDesrc check
        result3=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.1.1.0')
        if result3 == dut.sysDescr:
            print(f"sysDescr: {result3}(Passed!!)")
        else:
            print(f"sysDescr: {result3}(Failed!!)")
        # 4. docsDevSwCurrentVers check
        result4=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.69.1.3.5.0')
        if result4 == dut.sw:
            print(f"docsDevSwCurrentVers: {result4}(Passed!!)")
        else:   
            print(f"docsDevSwCurrentVers: {result4}(Failed!!)")
        # 5. Completeness of ifTable
        result5=await my_snmp.my_snmp_walk(my_logger,oid='1.3.6.1.2.1.2.2',end_oid='1.3.6.1.2.1.4.1')
        ##把iftable結果存入txt檔，並以MAC分類
        
        with open(rf'D:\Data\python\CD8021_ifTable\{mac}_{docsis}_{d_ver}_ifTable.txt', 'a') as f:
            f.write(f"ifTable for {mac}:\n")
            f.write(f"{result5}\n")
        print("ifTable writing(Successed!!)\n----------------------------------------------------------------------------")
    except Exception as e:
        print(f"An error occurred: {e}(Failed!!)\n----------------------------------------------------------------------------")



if __name__ == "__main__":

    asyncio.run(sample_test())
