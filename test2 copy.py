import os,logging,asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
# def test():
    # os.makedirs('log',exist_ok=True)
    # logger = logging.getLogger(__name__)
    # # 取得【年月日時分】的字串，作為檔名的一部分。
    # date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # # 設定工作日誌檔的檔名、欄位及內碼，及要寫入的等級
    # logging.basicConfig(filename=f'log/{date_time}.log', 
    # format='%(asctime)s %(levelname)s:%(message)s', datefmt='%I:%M:%S', 
    # encoding='utf-8', level=logging.DEBUG)
    # logging.debug("除錯")
    # logging.info("資訊")
    # logging.warning("警告")
    # logging.error("錯誤")
    # logging.critical("關鍵資訊")
async def test():
            """testing ifTable can access"""
            snmpEngine = SnmpEngine()
            result=  walk_cmd(
                        snmpEngine,
                        CommunityData('private',mpModel=1),
                        await UdpTransportTarget.create(('172.16.160.24', 161)),
                        # await UdpTransportTarget.create(('172.16.160.30', 161)),
                        ContextData(),
                        ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2')),
                        lexicographicMode=False
                        )
            g = [item async for item in result]
            end=''
            i=0
            while end!='1.3.6.1.2.1.4.1' and i < len(g):    
                for d in g[i][3]:
                        end = d[0]
                        print(f"{d[0]}={d[1].prettyPrint()}")
                        i+= 1
           
            
            snmpEngine.close_dispatcher()
            
         
asyncio.run(test())