import asyncio
import telnetlib3
import error_statement,re,telnet_operation

async def telnet_conn(cmts,dut_mac,operation='bpi'):
    """Telnet to CMTS to get the information"""
    # Server details
    port = 23 
    match cmts:
        case "172.16.1.9": 
            # login informations for each cmts written in list
            login_info=["root","casa","en","casa"]
        case "172.16.1.6":
            # login informations for each cmts written in list
            login_info=["root","casa","en","casa"]
        case "172.16.1.15":
            login_info=["admin","harmonic1","ssh admin@172.16.1.18","nsgadmin"]
        case "172.16.1.10":
            login_info=["cisco","en","cisco"]

    try:
        # Establish the Telnet connection
        reader, writer = await telnetlib3.open_connection(host=cmts, port=port)
        print(f"Telnet connected to {cmts}:{port}")

        
        #Logging into different CMTS 
        for i in login_info:
            writer.write(f"{i}\n")
            await asyncio.sleep(0.5)

        #Operation 
        if operation=='bpi':
            writer.write(f"scm | inc {dut_mac}\n")  
            await asyncio.sleep(1)
            # CMTS response
            print("Telnet Server response:")
            response = await reader.read(1024) 
            bpi=response.find("online(pt)")
            if bpi==-1:
                print(f"BPI failed\n{response}")
            else:
                print("BPI successful!!")
        # Closing the connection
        writer.close()
        print("Telnet connection closed.")

    except Exception as e:
        print(f"Failed to connect to {cmts}:{port}")
        print(f"Error: {e}")

# Run the async Telnet client
if __name__=="__main__":
    asyncio.run(telnet_conn("172.16.1.15","08bd"))
