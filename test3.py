import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# 此段程式碼將 result 存入 D:\Data\pysnmp\result.txt中，若有錯誤產生，則不會存入result。

def store_statement(result):
    
        errorIndication, errorStatus, errorIndex, varBinds =  result
        if errorIndication:
            print(f"errorIndication:{errorIndication}\n")
        elif errorStatus:
            print(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
        else:
            # with open(r'D:\Data\pysnmp\result.txt',"a") as f:
            #     for varBind in varBinds:
            #         f.write(f"{varBind}\n")
            print("\n")
            with open(r'D:\Data\pysnmp\result.txt',"a") as f:    
                for varBind in varBinds:
                    tmp=str(varBind)
                    print(f"{tmp}\n------------------------------------")
                    f.write(f"{tmp}\n")
                    

