import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import os

class SNMPResultLogger:
    def __init__(self,Fw,test_name, base_path=r"D:\Data\pysnmp"):
        self.fw=Fw
        self.test_name=test_name
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
        """建立一個 TEST_NAME.txt"""
        self.folder_path = os.path.join(self.base_path, self.test_name)
        if not os.path.exists(self.folder_path): 
            try:
                os.makedirs(self.folder_path, exist_ok=True)
                print(f"File '{self.folder_path}' created successfully!")
            except Exception as e:
                print(f"When creating the file for results:\n{e}")

    def store_result(self, test_name, result):
        """儲存結果，分為一般文字以及SNMP的結果"""
        current_time = datetime.now().strftime("%Y_%m_%d")
        file_path = os.path.join(self.base_path, test_name,f"{current_time}.txt")
        # 一般文字
        if type(result)==str:
            try:
                with open(file_path, "a") as f:
                        f.write(f"{result}\n")
                        print("writting log success!")
                        return
            except Exception as e:
                print(f"Failed to write to file: {e}")
        # SNMP 結果
        errorIndication, errorStatus, errorIndex, varBinds = result
        if errorIndication:
            print(f"errorIndication: {errorIndication}\n")
        elif errorStatus:
            print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
        else:
            print(f"\nThe result of {test_name}:")
            try:
                with open(file_path, "a") as f:
                    for varBind in varBinds:
                        tmp = str(varBind)
                        print(f"{tmp}\n------------------------------------")
                        f.write(f"{tmp}\n")
            except Exception as e:
                print(f"Failed to write to file: {e}")
