import snmp_operation,asyncio,error_statement
class My_CD9030:
    def __init__(self,dut):
        self.test_case="CD9030"
        self.dut=dut
        self.logger=error_statement.SNMPResultLogger(dut.mac,self.test_case)
        self.logger.init_folder()

    async def test(self):
        test_case="test"
        logger1=error_statement.SNMPResultLogger("test_dut",test_case)
        logger1.init_folder()
        snmp1=snmp_operation.MySnmp(self.dut,"test_dut",test_case)

if __name__=="__main__":
    # Run the test
    # asyncio.run(test())
    pass
    
    