import paramiko

import sys

​

def cmdline(ssh, command):

    stdin, stdout, stderr = ssh.exec_command(command)

    err = stderr.read()

    return err

​

def combinations(words, length):

    if length == 0:

        return []

    result = [[word] for word in words]

    while length > 1:

        new_result = []

        for combo in result:

            new_result.extend(combo + [word] for word in words)

        result = new_result[:]

        length -= 1

    return result

​

def main():

    # Replace these variables with your own values

    host = "your_target_ip"  # e.g., "10.10.10.10"

    port = 22

    username = "your_username"

    password = "your_password"  # or use an RSA key for better security

    

    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    ssh.connect(host, port, username, password)

​

    words = [line.strip() for line in open('wl.lst')]

    s = b'writing RSA key\r\n'

    print("\n")

​

    res = combinations(words, 1)

    c = len(res) - 1

    for idx, result in enumerate(res):

        str1 = "openssl rsa -in ssl.key -out ssld.key -passin pass:" + result[0]

        if cmdline(ssh, str1) == s:

            print("\nKey Found! The key is: " + result[0])

            ssh.close()

            sys.exit()

        print(str(idx) + "/" + str(c))

    print("\n")

​

    res = combinations(words, 2)

    c = len(res) - 1

    for idx, result in enumerate(res):

        str1 = "openssl rsa -in ssl.key -out ssld.key -passin pass:" + result[0] + result[1]

        if cmdline(ssh, str1) == s:

            print("\nKey Found! The key is: " + result[0] + result[1])

            ssh.close()

            sys.exit()

        print(str(idx) + "/" + str(c))

    print("\n")

​

    res = combinations(words, 3)

    c = len(res) - 1

    for idx, result in enumerate(res):

        str1 = "openssl rsa -in ssl.key -out ssld.key -passin pass:" + result[0] + result[1] + result[2]

        if cmdline(ssh, str1) == s:

            print("\nKey Found! The key is: " + result[0] + result[1] + result[2])

            ssh.close()

            sys.exit()

        print(str(idx) + "/" + str(c))

    print("\n")

​

    res = combinations(words, 4)

    c = len(res) - 1

    for idx, result in enumerate(res):

        str1 = "openssl rsa -in ssl.key -out ssld.key -passin pass:" + result[0] + result[1] + result[2] + result[3]

        if cmdline(ssh, str1) == s:

            print("\nKey Found! The key is: " + result[0] + result[1] + result[2] + result[3])

            ssh.close()

            sys.exit()

        if idx % 25 == 0:

            print(str(idx) + "/" + str(c))

    print("\n")

​

    res = combinations(words, 5)

    c = len(res) - 1

    for idx, result in enumerate(res):

        str1 = "openssl rsa -in ssl.key -out ssld.key -passin pass:" + result[0] + result[1] + result[2] + result[3] + result[4]

        if cmdline(ssh, str1) == s:

            print("\nKey Found! The key is: " + result[0] + result[1] + result[2] + result[3] + result[4])

            ssh.close()

            sys.exit()

        if idx % 100 == 0:

            print(str(idx) + "/" + str(c))

    print("\n")

​

    ssh.close()

​

if __name__ == '__main__':

    main()

​
