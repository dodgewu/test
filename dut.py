class dut():
    def __init__(self,mac,cmts,ip,fw,test_case):
        # MAC後四碼
        self.mac=mac
        # 上線的CMTS
        self.cmts=cmts
        # DUT 被分配到的號碼
        self.ip=ip
        self.fw=fw
        self.test_case=test_case        


