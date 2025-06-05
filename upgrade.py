from pysnmp.hlapi.v3arch.asyncio import *
import error_statement
import snmp_operation
from pathlib import Path


async def snmp_upgrade(dut):
    """利用snmp來升降級fw"""
    try:
        test_case = 'NTLCH8568QE-2373'
        tftp_server=input("Please input the tftp server ip address: ")
        tftp_address=Path(input("Please input the tftp file address: "))
        my_logger = error_statement.SNMPResultLogger(dut, test_case)
        my_logger.init_folder()
        my_snmp = snmp_operation.MySnmp(dut, test_case,community='public')
        result= await my_snmp.my_snmp_set(my_logger,'1.3.6.1.2.1.69.1.3.1.0',tftp_server)
        for i in result:
            print(f"{i.prettyPrint()}")
        result= await my_snmp.my_snmp_set(my_logger,'1.3.6.1.2.1.69.1.3.2.0',tftp_address)
        for i in result:
            print(f"{i.prettyPrint()}")
        result= await my_snmp.my_snmp_set(my_logger,'1.3.6.1.2.1.69.1.3.3.0',Integer32(1))
        for i in result:
            print(f"{i.prettyPrint()}")
    except Exception as e:
        print(f"There is an error occurred when running the upgrade: {e}")
    print("---------------------------------------------------------------")

