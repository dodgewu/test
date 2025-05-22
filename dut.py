class Dut():
    def __init__(self,mac,cmts,ip,fw,wifi_24_ver,wifi_55_ver):
        # MAC後四碼
        self.mac=mac
        # 上線的CMTS
        self.cmts=cmts
        # DUT 被分配到的IP
        self.ip=ip
        # 此次測試FW
        self.fw=fw
        self.wifi_24_ver=wifi_24_ver  
        self.wifi_55_ver=wifi_55_ver



