import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

# 此段程式碼將 result 存入

async def store_statement(result):
     
     with open(r'D:\Data\pysnmp\result.txt',"a") as f:
        errorIndication, errorStatus, errorIndex, varBinds = await result

        if errorIndication:
            f.write(f"errorIndication:{errorIndication}\n")

        elif errorStatus:
            f.write(f"Error Status: {errorStatus.prettyPrint()} at {errorIndex}\n")
        else:
            for varBind in varBinds:
                f.write(f"{varBind}\n")
# if __name__=="__main__":

#     store_statement()
