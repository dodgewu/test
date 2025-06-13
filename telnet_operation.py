import telnetlib3,asyncio
import error_statement,telnet_connection,dut,re,sys


class No_unprov_onu(Exception):
    """主要是ONU接上線後，OLT中沒有看到此裝置時發起。"""
    def __init__(self,*args):
        super().__init__(*args)

async def bpi(tel,dut,logger):
    """telnet_connection流程
        1. 建立連線
        2. 登入CMTS
        3. 輸入指令
        4. 讀取指令
        5. 分析資料
        6. 關閉連線"""
    await tel.tel_connection()
    await tel.logging()
    await tel.write_command("bpi")
    response=await tel.read_command()
    result=await result_analy(response,"bpi")
    logger.store_result(dut,response,explanation="BPI result in CMTS")
    await tel.connection_closed()
    return result


async def result_analy(response,oper):
        """用來分析結果"""
        if oper=='bpi':
            bpi=response.find("online(pt)")
            if bpi==-1:
                return False
            else:
                return True

async def OLT_provision(my_tel):
    """This function is for provision ONU in OLT with XGS-PON and HGU. 
        Step
    """
    try:
        await my_tel.tel_connection()
        await my_tel.login()
        # await delete_onu(my_tel)
        # await asyncio.sleep(10)
        my_tel.desc1=input("please enter your name for description1.(e.g. Sample1)\n")
        my_tel.desc2=input("please enter product name for description2.(e.g. FH5781)\n")
        my_tel.channel_pair, my_tel.serial_number=await xgh_discover(my_tel)
        await asyncio.sleep(2)
        my_tel.max_onu=await xgh_chk_onu(my_tel)
        await asyncio.sleep(2)
        await xgh_register_sn(my_tel)
        await asyncio.sleep(2)
        await xgh_configure_slot(my_tel)
        await asyncio.sleep(2)
        await xgh_configure_qos(my_tel)
        await asyncio.sleep(2)
        await xgh_configure_bridge(my_tel)
        await asyncio.sleep(2)   
    except No_unprov_onu as e:
        print(f"[ERROR]There is no unprovision-onu in OLT list\n{e}")
        sys.exit(1)
    except Exception as e:
        print(f"[ERROR]the error:{e}")
        sys.exit(1)
    finally:
        await my_tel.connection_closed()
async def xgh_discover(my_tel):
    """This function is for xgh_discover ONU in OLT with unprovision state. """
    command = r"show channel-pair unprovision-onu"
    await my_tel.write_command(command)
    response = await my_tel.read_command()
    if re.findall(fr'unprovision-onu\scount\s:\s0',response):
        raise No_unprov_onu()
    pattern= r"\d/\d/\d/\d\s{3}\w{4}\d{8}"
    result = re.findall(pattern, response)
    return result[0][0:7],result[0][10:25] 

async def xgh_chk_onu(my_tel):
    command= r"show equipment ont status channel-pair"
    await my_tel.write_command(command)
    response = await my_tel.read_command()
    pattern= fr"{my_tel.channel_pair}\s\s\sng2:\d/\d/\d*"
    result = re.findall(pattern, response)
    # OLT會以由小到大顯示出ONU，故最後一個會是最大值
    max_onu=result[-1][18:]
    return max_onu
    

async def xgh_register_sn(my_tel):
        tmp=[my_tel.serial_number[:4],":",my_tel.serial_number[4:13]]
        my_tel.serial_number="".join(tmp)
        tmp=["ng2:",my_tel.channel_pair[-1],"/1/",str(int(my_tel.max_onu)+1)]
        my_tel.onu="".join(tmp)
        command=rf'configure equipment ont interface {my_tel.onu} sw-ver-pland disabled sernum {my_tel.serial_number} fec-up enable pref-channel-pair {my_tel.channel_pair} enable-aes disable voip-allowed enable desc1 "{my_tel.desc1}" desc2 "{my_tel.desc2}"'
        await my_tel.write_command(command)
        command=rf"configure equipment ont interface {my_tel.onu} admin-state up"
        await my_tel.write_command(command)
        response = await my_tel.read_command()

async def xgh_configure_slot(my_tel):
    # 先找veip的 slot index, data port, and voice port.
    tmp=[]
    while not tmp:
        await asyncio.sleep(5)
        command=r"show equipment ont slot"
        await my_tel.write_command(command)
        response = await my_tel.read_command()
        pattern=rf"{my_tel.onu}/\d\s\s\s\s\s\d\s\s\s\s\s\s\s\s\s\s\d\s\s\s\s\s\s\s\s\s\s\sveip"
        tmp=re.findall(pattern,response)
    posi=len(my_tel.onu)
    my_tel.ont_slot=tmp[0][:posi+2]
    my_tel.data_port=tmp[0][posi+7]
    my_tel.voice_port=tmp[0][posi+18]
    # state up veip 功能
    command=[rf'configure equipment ont slot {my_tel.ont_slot} planned-card-type veip plndnumdataports {my_tel.data_port} plndnumvoiceports {my_tel.voice_port} admin-state up',rf'configure veip ont {my_tel.ont_slot}/1 admin-state up']
    await my_tel.write_command(command[0])
    await my_tel.write_command(command[1])
    response = await my_tel.read_command()

async def xgh_configure_qos(my_tel):
    command=rf'configure qos interface uni:{my_tel.ont_slot}/1 scheduler-node name:CBN_XGS_PON cac-profile name:FD_ONTUniVideo ds-num-rem-queue not-applicable us-num-queue not-applicable'
    await my_tel.write_command(command)
    for i in range(0,8):
        command=fr'configure qos interface uni:{my_tel.ont_slot}/1 upstream-queue {i} bandwidth-profile name:CBN_XGS_PON bandwidth-sharing uni-sharing'
        await my_tel.write_command(command)
    response = await my_tel.read_command()

async def xgh_configure_bridge(my_tel):
    # default vlan 是100
    vlan='100' 
    command=[fr'configure bridge port {my_tel.ont_slot}/1 max-unicast-mac 128',fr'configure bridge port {my_tel.ont_slot}/1 vlan-id {vlan}',fr'configure bridge port {my_tel.ont_slot}/1 pvid {vlan}']
    for i in command:
        await asyncio.sleep(1)
        await my_tel.write_command(i)
        response = await my_tel.read_command()

async def delete_onu(my_tel):
     """待改，寫死給測試部件使用"""
     command=[r'configure equipment ont interface ng2:1/1/100 admin-state down',r'configure equipment ont no interface ng2:1/1/100']
     await my_tel.write_command(command[0])
     await my_tel.write_command(command[1])

async def test():
    test_case='test_telnet'
    my_dut=dut.Dut(mac='8e02',fw='Test')
    my_logger=error_statement.SNMPResultLogger(my_dut,test_case)
    my_logger.init_folder()
    test=telnet_connection.tel_connection(my_dut,"172.16.1.11")
    await OLT_provision(test)

asyncio.run(test())