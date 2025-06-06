import snmp_operation,asyncio,dut
from pysnmp.hlapi.v3arch.asyncio import *
async def main(dut):
    await asyncio.sleep(1)
if __name__=="__main__":
    my_dut=dut.Dut(ip='172.16.42.14',cmts='172.16.1.9',mac='f8fb',fw='Test',test_case='NTL7465LG_36',wifi_24_ver=None,wifi_55_ver=None)
    my_set=main(my_dut)
    asyncio.run(my_set.main())
