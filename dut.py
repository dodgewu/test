class Dut():
    def __init__(self,mac,cmts,ip,fw,**kwargs):
        # MAC後四碼
        self.mac=mac
        # 上線的CMTS
        self.cmts=cmts
        # DUT 被分配到的IP
        self.ip=ip
        # 此次測試FW
        self.fw=fw
        # 動態設定 keywords arguments
        for key,value in kwargs.items():
            setattr(self,key,value)

