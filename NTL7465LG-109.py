import subprocess,re
import error_statement

test_name="NTL7465LG_109"
# Concept : 
#     step1 check dual ip; ok
#     step2 testing content(ping); 
#     step3 restart dut; 
#     step4 testing content + ping 192.168.101.1

def test():
    # step1 : check DUT is in dual-mode(ipv4 and ipv6 both)
    shell_command='ipconfig'
    ip_mask='192.168.178'
    shell_result=str(subprocess.run(shell_command, shell=True, capture_output=True, text=True))

    statement1=error_statement.SNMPResultLogger('20280418_6.15.35eng-1-SH(NA)',test_name)
    statement1.init_folder()
    statement1.store_result(test_name,shell_result)
    cmd_result=cmd_anay(ip_mask)
    if cmd_result:
        print("step1 : DUT got dual ip  (pass)\n-------------------------------------------------")

def cmd_anay(ip):
    shell_result=str(subprocess.run('ipconfig', shell=True, capture_output=True, text=True))
    result=re.split(r'Wi-Fi',shell_result,1)
    try:
        if ip in result[1]:
            print(fr"you got the ip '{ip}.X'")
            return 1
        elif "媒體已中斷連線" in result[1]:
            print("you didn't get the ip.(媒體已中斷連線)")

    except ValueError as e:
        print(f"There is no WIFI interface\n{e}")
        
test()
