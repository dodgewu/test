import asyncio
from pysnmp.hlapi.v3arch.asyncio import *
import error_statement
async def test():
    # dut_ip=input("please enter an dut ip.\n")
    dut_ip='172.16.160.22'
    oid="1.3.6.1.4.1.35604.2.3.14.6.0"
    snmpEngine = SnmpEngine()
    g = get_cmd(
                snmpEngine,
                CommunityData('private'),
                # await UdpTransportTarget.create(('172.16.160.32', 161)),
                await UdpTransportTarget.create((str(dut_ip), 161)),
                ContextData(),
                # ObjectType(ObjectIdentity("SNMPv2-MIB", "sysDescr", 0)),
                ObjectType(ObjectIdentity(oid)),
                # ObjectType()
                )
    errorIndication, errorStatus, errorIndex, varBinds = await g
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
            # print(f"{oid}:\n")
            print(f"{varBind[0]}={varBind[1]}\n------------------------------------------------------------------")
            # print(" = ".join([x.prettyPrint() for x in varBind]))

    snmpEngine.close_dispatcher()

async def my_walk():
    # ip=str(input("please enter an ip to walk the mibs.\n"))
    ip='172.16.160.32'
    oid='1.3.6.1.4.1.35604.2.3.1.1.1.1.1.1'
    snmpEngine=SnmpEngine()
    w=walk_cmd(
        snmpEngine,
        CommunityData('private'),
        await UdpTransportTarget.create((ip,161)),
        ContextData(),
        ObjectType(ObjectIdentity(oid)),
        # 設定walk(getnext)個數
        maxRows=2017
    )
    async for walk_result in w:
        test_name="NTL7465LG-8299"
        statement1=error_statement.SNMPResultLogger("pheonix",test_name)
        statement1.init_folder()
        statement1.store_result(test_name,walk_result)
        # if errorIndication:
        #     print(errorIndication)

        # elif errorStatus:
        #     print(
        #         "{} at {}".format(
        #             errorStatus.prettyPrint(),
        #             errorIndex and varBinds[int(errorIndex) - 1][0] or "?",
        #         )
        #     )
        # else:
        #     for varBind in varBinds:
        #         print("{}\n------------------------------------------------------------------".format(varBind))    

    snmpEngine.close_dispatcher()
asyncio.run(test())