import asyncio
import telnetlib3
import error_statement,re,dut,sqlite3

#建立基本的telnet連線
class tel_connection:
    # def tel_oper(self,tmp):
    #     if tmp=="bpi":
    #         return f"scm | inc {self.dut_mac}\n"
    def __init__(self,dut,cmts,**kwargs):
        self.cmts=cmts
        self.dut_mac=dut.mac
        self.port=23
        self.writer=None
        self.reader=None
        self.login_info= self.get_login_info(self.cmts)
        for key,value in kwargs.items():
            setattr(self,key,value)
    def get_login_info(self,cmts):
        try:
            match cmts:
                case "172.16.1.9": 
                    # login informations for each cmts written in list
                    return ["root","casa","en","casa"]
                case "172.16.1.6":
                    # login informations for each cmts written in list
                    return ["root","casa","en","casa"]
                case "172.16.1.15":
                    return ["admin","harmonic1","ssh admin@172.16.1.18","nsgadmin"]
                case "172.16.1.10":
                    return ["cisco","en","cisco"]
                case "172.16.1.11":
                    return ["isadmin","ans#150"]
        except Exception as e:
            print(f"Something got wrong when getting CMTS logging info.\n{e}")
    async def login(self):
        if self.writer:
            for i in self.login_info:
                self.writer.write(f"{i}\n")
                await asyncio.sleep(0.5)
            if self.reader:
                print(await self.reader.read(1024))
    async def write_command(self,oper):
        # command=self.tel_oper(oper)
        # self.writer.write(command)  
        oper = oper + "\n"
        self.writer.write(oper)  
        await asyncio.sleep(1)
    async def read_command(self):
            response = await self.reader.read(10000)
            if 'invalid token' in response and self.cmts=='172.16.1.11':
                raise CommandError()
            print(response)
            return response
    async def connection_closed(self):
        self.writer.close()
        print("Telnet connection closed.")
    async def tel_connection(self):
        """基本連線到CMTS"""
        try:
            reader, writer =  await telnetlib3.open_connection(host=self.cmts, port=self.port)
            self.reader=reader
            self.writer=writer
            print(f"Telnet connected to {self.cmts}:{self.port}")
        except Exception as e:
            print(f"Failed to connect to {self.cmts}:{self.port}")
            print(f"Error: {e}")
    
class CommandError(Exception):
    def __init__(self, *args):
        super().__init__(*args)



# Run the async Telnet client
async def main():
    test_case='test_telnet'
    my_dut=dut.Dut(mac='8e02',fw='Test')
    my_logger=error_statement.SNMPResultLogger(my_dut,test_case)
    my_logger.init_folder()
    test=tel_connection(my_dut,"172.16.1.11")
    await develop_test(test)
async def develop_test(test):
    command = input("Enter command to execute: ")
    command=command.strip()
    await test.tel_connection()
    await test.logging()
    await test.write_command(command)
    await test.read_command()
    await test.connection_closed()
if __name__=="__main__":
    asyncio.run(main())
