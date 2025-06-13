import re,snmp_operation,error_statement,dut
from pysnmp.hlapi.v3arch.asyncio import *

# 此程式用來批量升級CD8021的韌體
def cmts_mac_table():
    str = """

c094.3525.42e5 172.16.150.40   C0/0/3/UB     w-online(pt)      389   0.00   2002   1   N
342c.c4ee.4281 ---             C0/0/5/U2     init(rc)          4     -0.50  2083   0   N
6802.b814.2207 172.16.150.30   C0/0/5/UB     w-online          5     -0.50  2080   0   N
6802.b897.deb4 172.16.150.10   C0/0/5/UB     w-online          10    -7.00  2080   1   N
6802.b811.7610 172.16.150.148  C0/0/5/U0     offline           12           2090   0   N
6802.b826.28ac 172.16.150.65   C0/0/5/U4     reject(pk)        18    -7.00  2092   0   Y
342c.c4af.146f ---             C0/0/5/U2     init(rc)          19    0.00   494    0   N
342c.c4a2.c397 172.16.150.38   C0/0/5/UB     w-online          98    0.00   2093   2   N
342c.c4df.2826 ---             C0/0/5/U1     init(rc)          861   0.00   494    0   N
342c.c4a2.548d 172.16.150.63   C0/0/5/p      w-reject(pk)      934   0.00   3932   0   Y
6802.b826.27e0 172.16.150.69   C0/0/5/p      w-online          935   0.00   3935   0   Y
342c.c4a2.5490 172.16.150.70   C0/0/5/U0     offline           938          2092   0   Y
342c.c4fe.090a ---             C0/0/5/U1     init(rc)          6593  0.00   2081   0   N
6802.b86c.11b4 172.16.150.32   C0/0/5/p      p-online(pt)      6598  -7.00  494    0   Y
b4f2.6763.b080 172.16.150.42   C0/0/7/UB     w-online(pt)      2019  0.00   2002   1   Y
342c.c4fe.162e 172.16.150.18   C0/0/7/UB     w-online(pt)      4591  0.00   2130   0   Y
342c.c4fe.15fa 172.16.150.19   C0/0/7/U2     offline           4592         2129   0   Y
342c.c4fe.15e8 172.16.150.20   C0/0/7/UB     w-online(pt)      4595  0.00   2131   0   Y
342c.c4fe.15f6 172.16.150.22   C0/0/7/UB     w-online(pt)      4597  0.00   2131   0   Y
342c.c4fe.160e 172.16.150.23   C0/0/7/UB     w-online(pt)      4599  0.00   2131   0   Y
342c.c4fe.15de 172.16.150.28   C0/0/7/UB     w-online(pt)      4612  0.00   2131   0   Y
342c.c4fe.1642 172.16.150.29   C0/0/7/UB     w-online(pt)      4614  0.00   2130   1   Y
342c.c4fe.1640 172.16.150.11   C0/0/7/UB     w-online(pt)      4622  0.00   2129   0   Y
342c.c4fe.15d0 172.16.150.26   C0/0/7/UB     w-online(pt)      4624  0.00   2131   0   Y
342c.c4fe.15f0 172.16.150.35   C0/0/7/UB     w-online(pt)      4647  0.00   2130   0   Y
342c.c4fe.162c 172.16.150.34   C0/0/7/U5     offline           4648         2130   0   Y
342c.c4fe.1622 172.16.150.16   C0/0/7/UB     w-online(pt)      4651  0.00   2131   0   Y
342c.c4fe.15e2 172.16.150.33   C0/0/7/U5     offline           4653         2132   0   Y
342c.c4fe.160c 172.16.150.13   C0/0/7/UB     w-online(pt)      4656  0.00   2131   0   Y
342c.c4fe.15ea 172.16.150.14   C0/0/7/UB     w-online(pt)      4657  0.00   2131   0   Y
342c.c4fe.15f4 172.16.150.27   C0/0/7/UB     w-online(pt)      4665  -0.50  2131   0   Y
342c.c4fe.161c 172.16.150.31   C0/0/7/UB     w-online(pt)      4666  0.00   2129   0   Y
342c.c4fe.1634 172.16.150.39   C0/0/7/UB     w-online(pt)      4670  0.00   2132   0   Y
342c.c4fe.1628 172.16.150.43   C0/0/7/UB     w-online(pt)      4674  0.00   2129   0   Y
342c.c4fe.163a 172.16.150.44   C0/0/7/UB     w-online(pt)      4677  0.00   2130   0   Y
342c.c4fe.15dc 172.16.150.45   C0/0/7/UB     w-online(pt)      4680  0.00   2129   0   Y
342c.c4fe.160a 172.16.150.46   C0/0/7/U2     offline           4681         2128   0   Y

342c.c4fe.15f2 172.16.150.47   C0/0/7/UB     w-online(pt)      4682  0.00   2131   0   Y
342c.c4fe.163e 172.16.150.48   C0/0/7/U1     offline           4684         2133   0   Y
342c.c4fe.15d6 172.16.150.49   C0/0/7/UB     w-online(pt)      4686  0.00   2129   0   Y
342c.c4fe.1604 172.16.150.50   C0/0/7/UB     w-online(pt)      4690  0.00   2130   0   Y
342c.c4fe.162a 172.16.150.51   C0/0/7/UB     w-online(pt)      4691  0.00   2130   0   Y
342c.c4fe.1636 172.16.150.52   C0/0/7/UB     w-online(pt)      4695  0.00   2131   0   Y
342c.c4fe.1602 172.16.150.53   C0/0/7/U3     offline           4697         2131   0   Y
342c.c4fe.1626 172.16.150.54   C0/0/7/UB     w-online(pt)      4699  0.00   2130   0   Y
342c.c4fe.1632 172.16.150.12   C0/0/7/UB     w-online(pt)      4766  0.00   2131   0   Y
342c.c4fe.1610 172.16.150.25   C0/0/7/UB     w-online(pt)      4767  0.00   2129   0   Y
342c.c4fe.163c 172.16.150.55   C0/0/7/UB     w-online(pt)      4769  0.00   208    0   Y
342c.c4fe.1616 172.16.150.56   C0/0/7/UB     w-online(pt)      4772  0.00   2129   0   Y
342c.c4fe.1612 172.16.150.57   C0/0/7/UB     w-online(pt)      4774  0.00   2129   0   Y
342c.c4fe.15d8 172.16.150.58   C0/0/7/UB     w-online(pt)      4776  0.00   2129   0   Y
342c.c4fe.15e6 ---             C0/0/7/U2     init(rc)          4818  -0.50  2129   0   N
342c.c4fe.1606 172.16.150.24   C0/0/7/UB     w-online(pt)      4823  0.50   2129   0   Y
5c35.3bde.ad01 172.16.150.15   C0/0/7/U7     offline           4837         1791   0   N

    """
    pattern = r'\b([0-9a-f]{4}\.[0-9a-f]{4}\.[0-9a-f]{4})\s+(\d{1,3}(?:\.\d{1,3}){3})\b'
    matches = re.findall(pattern, str, re.IGNORECASE)
    # 提取每個 MAC 位址的末四碼並與其索引（從 1 開始）組成元組
    mac_ip = [(mac.replace(".", "")[-4:],ip) for mac,ip in matches]
    return mac_ip
async def bulk_upgrade(ip_list,ver):
    if ver=='nor':
        for no,mac,ip in ip_list:
            try:
                # 設定SNMP的OID
                snmpEngine=SnmpEngine() 
                # reboot
                result= await set_cmd(snmpEngine,
                                CommunityData('private',mpModel=1),
                                await UdpTransportTarget.create((ip,161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.1.3.0'),Integer(1)),                                )
                
                # result= await set_cmd(snmpEngine,
                #                 CommunityData('private',mpModel=1),
                #                 await UdpTransportTarget.create((ip,161)),
                #                 ContextData(),
                #                 ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.1.0'),OctetString('172.16.1.233')),
                #                 ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.2.0'),OctetString(r'stanley\CD8021\fw\MNB1525 CD8021-NewPKI.img')),
                #                 )
                
                # result= await set_cmd(snmpEngine,
                #                 CommunityData('private',mpModel=1),
                #                 await UdpTransportTarget.create((ip,161)),
                #                 ContextData(),
                #                 ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.3.0'),Integer(1))                            )
                snmpEngine.close_dispatcher()
            except Exception as e :
                print(f"There is an error occured when setting the value of MIBs you assigned.{e}")
    elif ver=='mac':
            for no,mac,ip in ip_list:
                try:
                    # 設定SNMP的OID
                    snmpEngine=SnmpEngine() 
                    result= await set_cmd(snmpEngine,
                                    CommunityData('private',mpModel=1),
                                    await UdpTransportTarget.create((ip,161)),
                                    ContextData(),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.1.0'),OctetString('172.16.1.233')),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.2.0'),OctetString(r'stanley\CD8021\fw\MNB1525 CD8021-MAC-14-NewPKI.img')),
                                    )
                    result= await set_cmd(snmpEngine,
                                    CommunityData('private',mpModel=1),
                                    await UdpTransportTarget.create((ip,161)),
                                    ContextData(),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.3.0'),Integer(1))                            )
                    snmpEngine.close_dispatcher()
                except Exception as e :
                    print(f"There is an error occured when setting the value of MIBs you assigned.{e}")
 
async def bulk_upgrade_0529(ip_list,ver):
    if ver=='nor':
        for ip in ip_list:
            try:
                # 設定SNMP的OID
                snmpEngine=SnmpEngine() 
                result1= await set_cmd(snmpEngine,
                                CommunityData('private',mpModel=1),
                                await UdpTransportTarget.create((ip,161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.1.0'),IpAddress('172.16.1.233')),
                                ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.2.0'),OctetString(r'stanley\CD8021\fw\MNB1525 CD8021.img')),
                                )
                
                result= await set_cmd(snmpEngine,
                                CommunityData('private',mpModel=1),
                                await UdpTransportTarget.create((ip,161)),
                                ContextData(),
                                ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.3.0'),Integer(1)))
                a,b,c,d=  result
                print(f"{ip}:{d[0]}")
                snmpEngine.close_dispatcher()
            except Exception as e :
                print(f"There is an error occured when you are upgrading normal {e}")
    elif ver=='mac':
            for ip in ip_list:
                try:
                    # 設定SNMP的OID
                    snmpEngine=SnmpEngine() 
                    result1= await set_cmd(snmpEngine,
                                    CommunityData('private',mpModel=1),
                                    await UdpTransportTarget.create((ip,161)),
                                    ContextData(),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.1.0'),IpAddress('172.16.1.233')),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.2.0'),OctetString(r'stanley\CD8021\fw\MNB1525 CD8021-MAC-14.img')),
                                    )
                    result= await set_cmd(snmpEngine,
                                    CommunityData('private',mpModel=1),
                                    await UdpTransportTarget.create((ip,161)),
                                    ContextData(),
                                    ObjectType(ObjectIdentity('1.3.6.1.2.1.69.1.3.3.0'),Integer(1)))
                    a,b,c,d= result
                    print(f"{ip}:{d[0]}")
                    # print(f"{ip}:{d[0]}")
                    snmpEngine.close_dispatcher()
                except Exception as e :
                    print(f"There is an error occured when you are upgrading mac-14 {e}")
       
if __name__ == "__main__":
    ee=cmts_mac_table()
    for i,j in ee:
        if i=='162a':
            print("yes")
