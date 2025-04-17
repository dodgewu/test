import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

def check(iterator):
    errorIndication, errorStatus, errorIndex, varBinds = iterator
    if errorIndication:
            print(errorIndication)

    elif errorStatus:
                print(
                    "{} at {}".format(
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                    )
                )
    else:
                for varBind in varBinds:
                    print(" = ".join([x.prettyPrint() for x in varBind]))

if __name__=="__main__":
        check()