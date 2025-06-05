import telnetlib3
import error_statement



async def bpi(tel,dut,logger):
    """telnet_connection流程
        1. 建立連線
        2. 登入CMTS
        3. 輸入指令
        4. 讀取指令
        5. 分析資料
        6. 關閉連線"""
    await tel.tel_connection()
    await tel.logging()
    await tel.write_command("bpi")
    response=await tel.read_command()
    result=await result_analy(response,"bpi")
    logger.store_result(dut,response,explanation="BPI result in CMTS")
    await tel.connection_closed()
    return result


async def result_analy(response,oper):
        """用來分析結果"""
        if oper=='bpi':
            bpi=response.find("online(pt)")
            if bpi==-1:
                return False
            else:
                return True
       