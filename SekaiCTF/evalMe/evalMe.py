#!/usr/bin/env python3

from pwn import *


def evalFunction(evaluationString):
	array = evaluationString.split()

	if array[1] == b'+':
		answer = int(array[0]) + int(array[2])
	elif array[1] == b'-':
		answer = int(array[0]) - int(array[2])
	elif array[1] == b'/':
		answer = int(array[0]) / int(array[2])
	elif array[1] == b'*':
		answer = int(array[0]) * int(array[2])
		
	return answer

def start():
    p = remote("chals.sekai.team", 9000)
    return p

p = start()

p.recvuntil("flag :)")

evaluation = p.recv()
answer = evalFunction(evaluation)

p.sendline(str(answer))
correctStr = (p.recvuntil(b"correct\n"))

i = 1
while i<101:
	nextEvalString = p.recv()
	print(nextEvalString)
	answer = evalFunction(nextEvalString)
	p.sendline(str(answer))
	correctStr = (p.recvuntil(b"correct\n"))
	
	i = i+1

print(p.recvuntil("\r#"))
nextEvalString = p.recvuntil("\n")
print(nextEvalString)
answer = evalFunction(nextEvalString)
p.sendline(str(answer))
correctStr = (p.recvuntil(b"correct\n"))

	

p.interactive()
