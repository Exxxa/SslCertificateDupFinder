# Certificate Collection Tool by Pierre LOPEZ & Zacharie MOY

## Overview

This Python script is a powerful tool designed for collecting SSL certificates from a specified URL efficiently. It utilizes multiple threads and public proxy servers, including the ability to test the validity of SOCKS5, SOCKS4, and HTTP proxies before using them for certificate collection.

Additionally, the script provides functionality to extract public key moduli from the collected certificates. It can sort them, find and count duplicates, and create a new file without duplicates.

## Prerequisites

### Install the required dependencies:

- Python 3.x
- Requests library (`pip install requests`)
- Cryptography library (`pip install cryptography`)

## Usage

Good Proxies Testing:
The program prompts whether to create a 'Good_Proxies.txt' file. If the user chooses to do so, the program tests the provided proxies for reliability.

Certificate Collection:
The program then initiates the certificate collection process. It sends requests to the specified domains, retrieves the SSL/TLS certificates, and stores them for further analysis.

Public Key Extraction:
After collecting the certificates, the program extracts the public key information. This information is crucial for understanding the cryptographic algorithms used for securing the communication.

### Clone the repository:
```bash
git clone git@gitlab.esiea.fr:lopez/lopez-moy-crypto-project-40a.git
cd your_repository
```

## Prepare your proxy lists:

- Save your SOCKS5 proxies in a file named `SOCKS5.txt`.
- Save your SOCKS4 proxies in a file named `SOCKS4.txt`.
- Save your HTTP proxies in a file named `HTTP.txt`.

### Run the Flowscrap_Proxy script:

# **Important: THE FIRST SCRIPT TO BE RUN IS Flowscrap_Proxy and then PubKformater!!**

The script will prompt you for the number of threads to use for certificate collection. Additionally, it will ask if you want to create a 'Good_Proxies.txt' file. If not done at least once, say yes when asked to run the proxy tester in Flowscrap_Proxy.py.

If you chose to create a 'Good_Proxies.txt' file, the script will use the validated proxies to collect SSL certificates. The certificates will be saved in a 'Certificates' folder.

### Public Key Modulus Extraction:

After certificate collection, the script allows you to extract public key moduli, sort them, find and count duplicates, and create a new file without duplicates. Follow the prompts to complete the public key processing.

### Adjust Proxy File Names:

Adjust the proxy file names in the script if you use different names for your proxy files. Open the file "YOUR_PROXY_FILE_NAME.txt" and get the proxy list.

Example:
```bash
proxyList = file_opener("YOUR_PROXY_FILE_NAME.txt")
```

Modify the URL and other parameters according to your requirements.

Make requests with proxies to the specified URL
```bash
make_requests_with_proxies("https://example.com/", (i - 1) * round(size))
```