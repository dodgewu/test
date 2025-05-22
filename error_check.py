import asyncio
from pysnmp.hlapi.v3arch.asyncio import *

def check(iterator):
    errorIndication, errorStatus, errorIndex, varBinds =  iterator
    if errorIndication:
            print(errorIndication)
            return 0

    elif errorStatus:
                print(
                    "{} at {}".format(
                        errorStatus.prettyPrint(),
                        errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
                    )
                )
                return 0
    else:
        return 1

if __name__=="__main__":
        check()