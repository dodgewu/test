import dut
import asyncio
import NTL7465LG_36,NTL7465LG_1604,sample_test

async def main():
    # my_dut=dut.Dut(ip='172.16.42.14',cmts='172.16.1.9',mac='f8fb',fw='CH7465PGFW-NCIP-6.15.36-SH(EU)',test_case='NTL7465LG_36')
    # my_dut=dut.Dut(ip='172.16.42.14',cmts='172.16.1.9',mac='f8fb',fw='Test',test_case='NTL7465LG_1604',wifi_55_ver='5.32.004.3.0.0',wifi_24_ver='clr_host_pkg_4.32.004.3.0.0-012722')
    my_dut=dut.Dut(ip='172.16.160.11',cmts='172.16.1.6',mac='0bda',fw='Test',wifi_55_ver='5.32.004.3.0.0',wifi_24_ver='clr_host_pkg_4.32.004.3.0.0-012722')
    # original constructor's test_case need to be None. Set up after into test function.
    # test1604= NTL7465LG_1604.test(my_dut)
    # await test1604
    # test36= NTL7465LG_36.test(my_dut)
    # await test36
    test1604= NTL7465LG_1604.test(my_dut)
    await test1604
    # test8063= NTL7465LG_8063.test(my_dut)
    # await test8063

    my_dut=dut.Dut(ip='',cmts='172.16.1.6',mac='',fw='Sample_test_CW151',wifi_55_ver=None,wifi_24_ver=None)
    cd8021=sample_test.sample_test(my_dut)
    await cd8021


    

asyncio.run(main())

