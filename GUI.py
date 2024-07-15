import requests
import socket
import whois
import dns.resolver
from tkinter import *
from tkinter import ttk
from tabulate import tabulate

def get_website_info(url):
    # Get the IP address
    try:
        ip_address = socket.gethostbyname(url)
    except socket.gaierror:
        return "Error: Could not resolve domain"

    # Get the WHOIS information
    try:
        whois_info = whois.whois(url)
        whois_data = []
        for key, value in whois_info.items():
            whois_data.append([key, value])
    except Exception:
        whois_data = [["Error", "Error retrieving WHOIS information"]]

    # Get the DNS records
    try:
        records = {}
        record_types = ['A', 'AAAA', 'CNAME', 'MX', 'NS', 'TXT']
        for record_type in record_types:
            answers = dns.resolver.resolve(url, record_type)
            records[record_type] = [str(rdata) for rdata in answers]
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer):
        records = {"Error": ["Domain not found or no records found"]}
    except Exception as e:
        records = {"Error": [str(e)]}

    # Get the HTTP headers
    try:
        response = requests.get(f"http://{url}")
        http_headers = [[header, value] for header, value in response.headers.items()]
    except requests.exceptions.RequestException as e:
        http_headers = [["Error", str(e)]]

    return ip_address, whois_data, records, http_headers

def display_website_info():
    url = url_entry.get()
    ip_address, whois_data, dns_records, http_headers = get_website_info(url)

    ip_address_label.config(text=f"IP Address: {ip_address}")

    whois_treeview.delete(*whois_treeview.get_children())
    for row in whois_data:
        whois_treeview.insert("", "end", values=row)

    dns_treeview.delete(*dns_treeview.get_children())
    for record_type, records in dns_records.items():
        dns_treeview.insert("", "end", text=record_type, values=", ".join(records))

    http_treeview.delete(*http_treeview.get_children())
    for header, value in http_headers:
        http_treeview.insert("", "end", values=[header, value])

root = Tk()
root.title("Website Information Gathering Tool")

main_frame = Frame(root)
main_frame.pack(padx=20, pady=20)

url_label = Label(main_frame, text="Enter Website URL:")
url_label.grid(row=0, column=0, sticky=E)

url_entry = Entry(main_frame)
url_entry.grid(row=0, column=1, padx=10, pady=10)

submit_button = Button(main_frame, text="Get Information", command=display_website_info)
submit_button.grid(row=0, column=2, padx=10, pady=10)

ip_address_label = Label(main_frame, text="")
ip_address_label.grid(row=1, column=0, columnspan=3, pady=10)

tabs = ttk.Notebook(main_frame)
tabs.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="nsew")

whois_tab = ttk.Frame(tabs)
dns_tab = ttk.Frame(tabs)
http_tab = ttk.Frame(tabs)

tabs.add(whois_tab, text="WHOIS Information")
tabs.add(dns_tab, text="DNS Records")
tabs.add(http_tab, text="HTTP Headers")

whois_treeview = ttk.Treeview(whois_tab, columns=("Field", "Value"), show="headings")
whois_treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)
whois_treeview.heading("Field", text="Field")
whois_treeview.heading("Value", text="Value")

dns_treeview = ttk.Treeview(dns_tab, show="tree")
dns_treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)
dns_treeview.heading("#0", text="Record Type")
dns_treeview.column("#0", width=150)

http_treeview = ttk.Treeview(http_tab, columns=("Header", "Value"), show="headings")
http_treeview.pack(fill=BOTH, expand=True, padx=10, pady=10)
http_treeview.heading("Header", text="Header")
http_treeview.heading("Value", text="Value")

root.mainloop()
