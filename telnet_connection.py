import asyncio
import telnetlib3
import error_statement,re,telnet_operation

#建立基本的telnet連線
class tel_connection:
    def tel_oper(self,tmp):
        if tmp=="bpi":
            return f"scm | inc {self.dut_mac}\n"
        
    # If you want yo write a determination, wrtie an function but not method.
    # def result_check(self,response,oper):
    #     match oper:
    #         case "bpi":
    #             bpi=response.find("online(pt)")
    #             if bpi==-1:
    #                 print(f"BPI failed\n{response}")
    #                 return
    #             else:
    #                 print("BPI successful!!")
    def get_login_info(self,cmts):
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
        pass
    async def logging(self):
        if self.writer:
            for i in self.login_info:
                self.writer.write(f"{i}\n")
                await asyncio.sleep(0.5)
            if self.reader:
                print(await self.reader.read(1024))
    async def write_command(self,oper):
        command=self.tel_oper(oper)
        self.writer.write(command)  
        await asyncio.sleep(1)
    async def read_command(self):
            response = await self.reader.read(1024) 
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
    def __init__(self,dut):
        self.cmts=dut.cmts
        self.dut_mac=dut.mac
        self.port=23
        self.writer=None
        self.reader=None
        self.login_info= self.get_login_info(dut.cmts)


# Run the async Telnet client
# if __name__=="__main__":
#     test=tel_connection("172.16.1.6","0bda")
#     asyncio.run(test.main())
