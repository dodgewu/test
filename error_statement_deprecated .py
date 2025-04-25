import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
from datetime import datetime
import os



# 此段程式碼將 result 存入 D:\Data\pysnmp\result.txt中，若有錯誤產生，則不會存入result。
path= r"D:\Data\pysnmp"


def init_statement(Fw_name):
    new_folder=fr"{path}\{Fw_name}"
    try:
        os.makedirs(fr"{new_folder}", exist_ok=True)
        print(f"Folder '{new_folder}' created successfully!")
    except Exception as e:
        print(f"When creating the path to store the statement of test result:\n{e}")
     
def store_statement(test_name,result):
        #Get the current time (e.g. 2025_04_25)
        current_time = datetime.now()
        my_current_time = current_time.strftime("%Y_%m_%d")

        errorIndication, errorStatus, errorIndex, varBinds =  result
        if errorIndication:
            print(f"errorIndication:{errorIndication}\n")
        elif errorStatus:
            print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
        else:
            print(f"\nThe result of {test_name} :")
            try:
                with open(fr'{path}\{my_current_time}.txt',"a") as f:    
                    for varBind in varBinds:
                        tmp=str(varBind)
                        print(f"{tmp}\n------------------------------------")
                        f.write(f"{tmp}\n")
            except Exception as e:
                print(f"Failed to write to file: {e}")
                 

