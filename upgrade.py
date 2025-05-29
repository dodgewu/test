from pysnmp.hlapi.v3arch.asyncio import *
import error_statement
import snmp_operation


async def snmp_upgrade(dut):
    test_case = 'upgrade_test'
    my_logger = error_statement.SNMPResultLogger(dut, test_case)
    my_logger.init_folder()
    my_snmp = snmp_operation.MySnmp(dut, test_case)
    result= await my_snmp.my_snmp_set(my_logger,'1.3.6.1.2.1.69.1.3.1.0',IpAddress('172.16.42.10'))
    print(result[0])

