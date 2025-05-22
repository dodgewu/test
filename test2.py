import os,logging
from datetime import datetime
def test():
    os.makedirs('log',exist_ok=True)
    logger = logging.getLogger(__name__)
    # 取得【年月日時分】的字串，作為檔名的一部分。
    date_time = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    # 設定工作日誌檔的檔名、欄位及內碼，及要寫入的等級
    logging.basicConfig(filename=f'log/{date_time}.log', 
    format='%(asctime)s %(levelname)s:%(message)s', datefmt='%I:%M:%S', 
    encoding='utf-8', level=logging.DEBUG)
    logging.debug("除錯")
    logging.info("資訊")
    logging.warning("警告")
    logging.error("錯誤")
    logging.critical("關鍵資訊")
test()