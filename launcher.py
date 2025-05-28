import dut
import asyncio
import NTL7465LG_36,NTL7465LG_1604,sample_test
import test

async def main():
    #CD8021 submission
    # 原始的 MAC 位址列表
    mac_string = """34:2C:C4:FE:16:2A
    34:2C:C4:FE:16:3E
    34:2C:C4:FE:16:42
    34:2C:C4:FE:15:DE
    34:2C:C4:FE:15:D0
    34:2C:C4:FE:15:F2
    34:2C:C4:FE:16:26
    34:2C:C4:FE:16:3C
    34:2C:C4:FE:15:D8
    34:2C:C4:FE:16:12
    34:2C:C4:FE:16:02
    34:2C:C4:FE:16:0C
    34:2C:C4:FE:15:F0
    34:2C:C4:FE:16:0A
    34:2C:C4:FE:15:FA
    34:2C:C4:FE:16:2E
    34:2C:C4:FE:15:DC
    34:2C:C4:FE:16:32
    34:2C:C4:FE:16:3A
    34:2C:C4:FE:15:F6
    34:2C:C4:FE:16:22
    34:2C:C4:FE:16:0E
    34:2C:C4:FE:16:2C
    34:2C:C4:FE:16:16
    34:2C:C4:FE:15:E2
    34:2C:C4:FE:16:40
    34:2C:C4:FE:15:E8
    34:2C:C4:FE:15:D6
    34:2C:C4:FE:16:10
    34:2C:C4:FE:16:04
    34:2C:C4:FE:16:06
    34:2C:C4:FE:16:28
    34:2C:C4:FE:15:EA
    34:2C:C4:FE:16:36
    34:2C:C4:FE:15:F4
    34:2C:C4:FE:16:1C
    34:2C:C4:FE:16:34
    34:2C:C4:FE:16:00"""
    # 將 MAC 位址字串分割成列表，每行一個 MAC 位址
    mac_addresses = mac_string.splitlines()

# 提取每個 MAC 位址的末四碼並與其索引（從 1 開始）組成元組
    mac = [(mac.replace(":", "")[-4:]) for mac in mac_addresses]
    no=['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27', '28','31','32','34','36', '37', '38', '39', '40', '41', '42']
    indexed_last_four=[]
    for i in range(len(mac)):
        indexed_last_four.append((no[i], mac[i]))


    mac_ip=test.cmts_mac_table()
    
    result = [(i[0], i[1], j[1]) for i in indexed_last_four for j in mac_ip if i[1].lower() == j[0].lower() ]
    
    ug=input("Do you want to upgrade FW\n")
    if ug =="normal":
        await test.bulk_upgrade(result,"nor")

    if ug=="mac14":
        await test.bulk_upgrade(result,"mac")
    #test
    sysDescr='DOCSIS 3.1 Cable Modem <<HW_REV: V1.0; VENDOR: Compal Broadband Networks; BOOTR: 2.8.47alpha0; SW_REV: Cert_24.2.0.4; MODEL: MNB1525 CD8021>>'
    sw='Cert_24.2.0.4'
    for index,mac,ip in result:
        my_dut=dut.Dut(ip=ip,cmts='172.16.1.10',mac=mac,fw='Sample_test_CW151',no=index,sysDescr=sysDescr,sw=sw)    
        cd8021=sample_test.sample_test(my_dut,(index,mac,ip))
        await cd8021



asyncio.run(main())

