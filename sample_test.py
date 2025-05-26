import asyncio,dut,error_statement,snmp_operation
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import os, logging 

async def sample_test(dut):
    # 1. 獲取ehternet mac
    # 2. 獲取hfc mac
    # 3. sysDesrc check 
    # 4. docsDevSwCurrentVers check 
    # 5. Completeness of ifTable
    # 6. get SN number 
    try:
        test_case='CD8021'
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
        if result3 != '':
            print("sysDescr (Failed!!)")
        else:
            print(f"sysDescr: {result3}(Passed!!)")
        # 4. docsDevSwCurrentVers check
        result4=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.69.1.3.5.0')
        if result4 != '':
            print("docsDevSwCurrentVers Failed!!")
        else:   
            print(f"docsDevSwCurrentVers: {result4}(Passed!!)")
        # 5. Completeness of ifTable
        result5=await my_snmp.my_snmp_walk(my_logger,oid='1.3.6.1.2.1.2.2',end_oid='1.3.6.1.2.1.4.1')
        
        # 6. get SN number
        result6=await my_snmp.my_snmp_get(my_logger,oid='1.3.6.1.2.1.69.1.1.4.0')
        if result6 != '':
            print("docsDevSerialNumber (Failed!!)")
        else:
            print(f"docsDevSerialNumber: {result6}(Passed!!)")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":

    asyncio.run(sample_test())
