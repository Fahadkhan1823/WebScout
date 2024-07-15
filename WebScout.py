import requests
import socket
import whois
import dns.resolver
import click
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

@click.command()
@click.option('--url', prompt='Enter the website URL', help='The URL of the website to gather information about')
def main(url):
    ip_address, whois_data, dns_records, http_headers = get_website_info(url)

    click.echo(f"IP Address: {ip_address}")

    click.echo("\nWHOIS Information:")
    click.echo(tabulate(whois_data, headers=['Field', 'Value']))

    click.echo("\nDNS Records:")
    for record_type, records in dns_records.items():
        click.echo(f"{record_type} Records: {', '.join(records)}")

    click.echo("\nHTTP Headers:")
    click.echo(tabulate(http_headers, headers=['Header', 'Value']))

if __name__ == "__main__":
    main()

