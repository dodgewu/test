import asyncio, telnetlib3

async def shell(reader, writer):
    # cm_mac=input("Plz enter a modem ip")
    cm_mac="08bd"
    while True:
        # read stream until '?' mark is found
        outp = await reader.read()
        if not outp:
            # End of File
            break
        elif 'CASA-C10G login' in outp:
            # reply all questions with 'y'.
            writer.write('root\r\n')
        elif 'Password' in outp:
            writer.write('casa\r\n')
        elif 'CASA-C10G>' in outp:
            if 'Password:' in outp:
                writer.write('casa\r\n')
            writer.write('en\r\n')
        elif 'CASA-C10G#' in outp:
            writer.write(f'scm | inc {cm_mac}\r\n')
            outp = await reader.readline()
            print(outp, flush=True)
            
        # display all server output
    print(outp, flush=True)
   
    # EOF
    print()
loop = asyncio.get_event_loop()
coro = telnetlib3.open_connection('172.16.1.9', 23, shell=shell)
reader, writer = loop.run_until_complete(coro)
loop.run_until_complete(writer.protocol.waiter_closed)