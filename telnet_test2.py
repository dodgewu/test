import asyncio
import telnetlib3
import error_statement

async def telnet_client():
    # Server details
    host = "172.16.1.9"  # Target IP address
    port = 23            # Telnet default port
    login='root'
    password='casa'
    en='en'
    dut_mac='08bd'

    try:
        # Establish the Telnet connection
        reader, writer = await telnetlib3.open_connection(host=host, port=port)
        print(f"Telnet connected to {host}:{port}")

         # Read data until the newline character

        writer.write(f"{login}\n")
        await asyncio.sleep(0.5)
        writer.write(f"{password}\n")
        await asyncio.sleep(0.5)
        writer.write(f"{en}\n")
        await asyncio.sleep(0.5)
        writer.write(f"{password}\n")
        response = await reader.read(1024) 
        writer.write(f"scm | inc {dut_mac}\n")
        await asyncio.sleep(1)
        
    
        
        print("Telnet Server response:")
        response = await reader.read(1024) 
        print(response)
        statment1=error_statement.SNMPResultLogger("20280418_6.15.35eng-1-SH(NA)","NTL7465LG_860")
        statment1.init_folder()
        statment1.store_result('NTL7465LG_860',response)
     
       
        # Closing the connection gracefully
        writer.close()
        print("Telnet connection closed.")

    except Exception as e:
        print(f"Failed to connect to {host}:{port}")
        print(f"Error: {e}")

# Run the async Telnet client
asyncio.run(telnet_client())
