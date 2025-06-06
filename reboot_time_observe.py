import os,logging,asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from pysnmp.hlapi import *
from datetime import datetime

# ***********************************************************************************************
# **  要改寫 sysUpTimeInstance 是DUT在CMTS上的時間，不是實際reboot time.
# **    應該用reboot 後時間相減。
# ***********************************************************************************************
# 目的:此code 用來觀察DUT reboot time 的時間。
# 步驟:
#     1. snmp reboot.
#     2. 等待DUT 已經在reboot.(CH8568LG reboot process 會有時間差)
#     3. 每15秒發送snmp_get 看sysUpTimeInstance 有無回應。若無則重複此步驟。
#     4. 若DUT有回應，則顯示出 sysUpTimeInstance 的時間。
# 參數調整:
#     1. step2.的 reboot process time, CH8568LG是大約30，所以等待30a秒後再snmp_get。


async def get():
            """用來抓取sysUpTimeInstance的值，並給analyze_result()分析結果。
            若有值，則返回"True,當前時間, sysUpTimeInstance的值"。"""
            cur = datetime.now()
            snmpEngine = SnmpEngine()
            result=  await get_cmd(
                        snmpEngine,
                        CommunityData('public',mpModel=1),
                        await UdpTransportTarget.create(('172.16.42.10',161),timeout=1),
                        ContextData(),
                        # sysUpTimeInstance: 1.3.6.1.2.1.1.3.0
                        ObjectType(ObjectIdentity('1.3.6.1.2.1.1.3.0')),
                        )
            tmp=analyze_result(result)
            snmpEngine.close_dispatcher()
            if tmp:
                return True,cur,tmp
            return False,cur,None
async def set():
        """reboot DUT用的。"""
        snmpengine=SnmpEngine()
        result=await set_cmd(snmpengine,CommunityData('public',mpModel=1),
                             await UdpTransportTarget.create(('172.16.42.10', 161)),
                             ContextData(),
                             ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.1.3.0'),Integer32(1)))
        errorIndication, errorStatus, errorIndex, varBinds = result
        if errorIndication:
            print(f"{errorIndication} \nreboot error.")
        elif errorStatus:
            print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
        elif errorIndex:
                print(f"Error Index: {errorIndex}\n")
        else:
            pass
        snmpengine.close_dispatcher()

def analyze_result(result):
    """用來分析get_cmd的結果。若無回應，則errorIndication 有值，若有回應，則回傳varbind。"""
    errorIndication, errorStatus, errorIndex, varBinds = result
    if errorIndication:
        print(f"{errorIndication}")
    elif errorStatus:
        print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
    elif errorIndex:
            print(f"Error Index: {errorIndex}\n")
    else:
        tmp=None
        for i in varBinds:
            tmp=i[1]
        return tmp
def time_format(result):
    """snmp response type is timeticks. transform into mm:ss"""
      
    time=float(result.prettyPrint())/100
    mins= int(time // 60)
    secs= int(time % 60)
    print('dut is connected.')
    print(f'sysUpTimeInstance: {mins} minutes and {secs} seconds')
def current_time():
    """return current time"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

async def main():

    start = datetime.now()
    print(f"{start.strftime("%Y-%m-%d %H:%M:%S")} Rebooting dut...")
    await set()
    # CH8568 reboot processing time 要大約30seconds。然後每15秒檢查一次是否重啟完成
    await asyncio.sleep(30)
    print("starting snmp request for every 15 seconds...")
    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"{current_time}")

        # a:dut有無回應，b:回應的時間, c:回應的內容 sysuptime(type timeticks)
        a,b,c=await get()
        await asyncio.sleep(8)
        if a==True:
            time_format(c)
            break

asyncio.run(main())