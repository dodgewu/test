import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import os

class SNMPResultLogger:
    def __init__(self,dut,test_case, base_path=r"D:\Data\pysnmp"):
        self.fw=dut.fw
        self.test_case=test_case
        self.base_path = fr"{base_path}\{self.fw}"
        self._ensure_base_path()

    def _ensure_base_path(self):
        #目的:建立基礎的folder path，範例 D:\Data\pysnmp\FW_NAME
        if not os.path.exists(self.base_path):
            try:
                os.makedirs(self.base_path)
                print(f"Base path '{self.base_path}' created.")
            except Exception as e:
                print(f"Error creating base path: {e}")

    def init_folder(self):
        """建立一個 test_case.txt"""
        self.folder_path = os.path.join(self.base_path, self.test_case)
        if not os.path.exists(self.folder_path): 
            try:
                os.makedirs(self.folder_path, exist_ok=True)
                print(f"File '{self.folder_path}' created successfully!")
            except Exception as e:
                print(f"When creating the file for results:\n{e}")

    def store_result(self, dut, result,explanation=None):
        """儲存結果，分為一般文字以及SNMP object的結果"""
        yymmdd = datetime.now().strftime("%Y_%m_%d")
        hhmmss = datetime.now().strftime("%H:%M:%S")
        file_path = os.path.join(self.base_path, self.test_case,f"{yymmdd}.txt")
        # 一般文字
        if isinstance(result,str):
            try:
                with open(file_path, "a",encoding="utf-8") as f:

                        f.write(f"[{hhmmss}]{result}\n")
                        f.write(f"----------------------------------------------------------------------------------")
                        return True
            except Exception as e:
                print(f"Failed to write to file: {e}")
        # SNMP 結果
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
# if __name__=='__main__':
#     statement1=error_statement.SNMPResultLogger(dut.fw,dut.test_case)
#     statement1.init_folder()
#     statement1.store_result(dut.test_case,result)