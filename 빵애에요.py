"""Problem Description
You are tasked with writing a Python script to identify valid subdomains for a given domain. 
Your script will take a domain name as a command-line argument and check a list of potential subdomains 
from a file named subdomains.txt. For each potential subdomain, the script should attempt to make an 
HTTP request and identify which subdomains are valid by checking if the request succeeds."""

import requests
import sys

# Ensure the user provides a domain as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <domain>")
    sys.exit(1)

# Read the list of subdomains from the file
with open("subdomains.txt") as file:
    subdoms = file.read().splitlines()

# Get the target domain from the command-line argument
target = sys.argv[1]

# Initialize a list to collect valid subdomains
valid_subdomains = []

# Iterate over the list of subdomains and check each one
for sub in subdoms:
    targeting = "https://{}.{}".format(sub, target)
    
    try:
        # Attempt to make an HTTP request to the subdomain
        r = requests.get(targeting)
        
        # Check if the request was successful
        if r.status_code == 200:
            valid_subdomains.append(targeting)
    except requests.ConnectionError:
        # Skip the subdomain if there is a connection error
        pass

# Print out the valid subdomains
for valid_sub in valid_subdomains:
    print("Valid domain:", valid_sub)

import requests
import sys

# Ensure the user provides a domain as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python script.py <domain>")
    sys.exit(1)

# Read the list of directories from the file
with open("directories.txt") as file:
    direcs = file.read().splitlines()

# Get the target domain from the command-line argument
target = sys.argv[1]
valid_directories = []

# Iterate over the list of directories and check each one
for dire in direcs:
    url = f"https://{target}/{dire}"

    try:
        r = requests.get(url)

        if r.status_code == 200:
            valid_directories.append(url)
    except requests.ConnectionError:
        # Skip the directory if there is a connection error
        pass

# Print out the valid directories
for valid_dire in valid_directories:
    print("Valid directory:", valid_dire)

import requests

# Read the list of URLs from the file
with open("urls.txt") as file:
    urls = file.read().splitlines()

valid_urls = []

# Iterate over the list of URLs and check each one
for url in urls:
    try:
        r = requests.get(url)
        print(f"{url} - Status Code: {r.status_code}")

        if r.status_code == 200:
            valid_urls.append(url)
    except requests.ConnectionError:
        print(f"{url} - Failed to connect")

# Print out the valid URLs
for valid_url in valid_urls:
    print("Status code 200 URL:", valid_url)
