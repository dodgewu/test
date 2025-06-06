class Dut():
    # def __init__(self,mac,**kwargs):
    def __init__(self,mac,cmts,ip,fw,**kwargs):
        # MAC後四碼
        self.mac=mac

        # 動態分配 cmts及ip
        self.cmts=cmts
        self.ip=ip
        # 此次測試FW
        self.fw=fw
        # 動態設定 keywords arguments
        for key,value in kwargs.items():
            setattr(self,key,value)

