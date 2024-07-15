# WebScout
The WebScout Tool is a Python-based application that allows users to gather various types of information about a website, including:
IP Address: The tool retrieves the IP address of the website.
WHOIS Information: The tool retrieves the WHOIS information for the website, which includes details such as the registrant, creation date, and expiration date.
DNS Records: The tool retrieves the DNS records for the website, including A, AAAA, CNAME, MX, NS, and TXT records.
HTTP Headers: The tool retrieves the HTTP headers for the website.
The tool uses several Python libraries, including requests, socket, whois, dns.resolver, click, and tabulate, to gather the information and present it in a user-friendly format.
The tool is designed to be run from the command line using the click library, which provides a simple and intuitive interface for users to enter the website URL and view the gathered information.
# How to install tool
## 1. Clone the repository
````
  git clone <Insert Link>
````
## 2. Enter into the directory
````
cd WebScout
````
## 3. Execute the command
````
python3 WebScout.py
````
## 4. For GUI, execute the command
````
python3 GUI.py
````
