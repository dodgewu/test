import dut
import asyncio
import NTL7465LG_36

async def main():
    my_dut=dut.dut(ip='172.16.160.22',cmts='172.16.1.6',mac='0be0',fw='CH7465PGFW-NCIP-6.15.36-SH',test_case='NTL7465LG_36')
    test36= NTL7465LG_36.test(my_dut)
    await test36

asyncio.run(main())

