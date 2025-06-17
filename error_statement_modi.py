import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import os,logging
# for testing
import dut

class SNMPResultLogger:
    def __init__(self,dut,test_case, base_path=r"D:\Data\pysnmp"):
        self.fw=dut.fw
        self.test_case=test_case
        self.base_path=os.path.join(base_path,self.fw)
        self._ensure_base_path()

    def _ensure_base_path(self):
        r"""目的:建立基礎的folder path，範例 D:\Data\pysnmp\FW_NAME"""
        # 若不存在該資料夾的話，新建一個。若已存在，則不動作。
        if not os.path.exists(self.base_path):
            try:
                os.makedirs(self.base_path)
                print(f"Base path '{self.base_path}' created.")
            except Exception as e:
                print(f"Error creating base path: {e}")

    def init_log(self):
        """建立一個 log 的文件"""
        self.folder_path = os.path.join(self.base_path, self.test_case)
        if not os.path.exists(self.folder_path): 
            try:
                os.makedirs(self.folder_path, exist_ok=True)
                print(f"File '{self.folder_path}' created successfully!")
            except Exception as e:
                print(f"When creating the file for results:\n{e}")

    def store_result(self, dut, result,explanation=None):
        """儲存結果，result 分為一般文字以及SNMP object"""
        yymmdd = datetime.now().strftime("%Y_%m_%d")
        hhmmss = datetime.now().strftime("%H_%M_%S")
        file_path = os.path.join(self.base_path, self.test_case,f"{yymmdd}.txt")
        
        # 一般文字
        if isinstance(result,str):
            # try:
            #     with open(file_path, "a",encoding="utf-8") as f:

            #             f.write(f"[{hhmmss}]{result}\n")
            #             f.write(f"----------------------------------------------------------------------------------")
            #             return True
            # except Exception as e:
            #     print(f"Failed to write to file: {e}")
            my_logger=logging.getLogger(__name__)
            logging.basicConfig(filename=file_path,filemode='w',datefmt='%Y-%m-%d %H:%M:%S',format='[%(asctime)s] %(message)s')
            my_logger.setLevel(logging.DEBUG)
            my_logger.debug(result)
            print("Logging File successed!!")
            return
        # SNMP 結果
        if asyncio.iscoroutine(result):

            errorIndication, errorStatus, errorIndex, varBinds = result
            if errorIndication:
                f.write(f"[{hhmmss}]{self.fw}-{self.test_case}:\nerrorIndication: {errorIndication}\n")
                print(f"errorIndication: {errorIndication}\n")
            elif errorStatus:
                f.write(f"[{hhmmss}]{self.fw}-{self.test_case}:\nError Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
                print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
            else:
                # print(f"\nThe result of {self.fw}-{dut.mac}-{self.test_case}:(SNMP)")
                try:
                    with open(file_path, "a",encoding="utf-8") as f:
                        # varBind[0]:oid, varBind[1]:value
                        for varBind in varBinds:
                            # print(f"{self.fw}-{self.test_case}:\n")
                            # print(f"{varBind[0]}={varBind[1]}\n------------------------------------")
                            f.write(f"<{dut.mac}:>\n")
                            f.write(f"[{hhmmss}]{varBind[0]}={varBind[1].prettyPrint()}\n")
                            f.write(f"----------------------------------------------------------------------------------\n")
                except Exception as e:
                    print(f"Failed to write to file: {e}")
    
# Please add the test code for the error_statement.py main function.
if __name__=='__main__':
    testing_dut=dut.Dut('EEEE',fw='TEST_LOGGING_NO_FW')
    statement1=SNMPResultLogger(testing_dut,test_case='logging_test')
    statement1.init_log()
    statement1.store_result(testing_dut,"logging test")
