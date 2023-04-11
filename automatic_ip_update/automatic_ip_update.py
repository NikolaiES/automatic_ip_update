import os
from urllib.parse import urlunparse
import json

from requests import get, request
import argparse


def update_domain(key, secret, ip, domain, subdomain):
    data = json.dumps([{
        "data": f"{ip}",
        "name": f"{subdomain}",
        "type": "A"
    }])
    url = urlunparse(("https", "api.godaddy.com", f"v1/domains/{domain}/records/A/{subdomain}", "", "", ""))
    headers = {
        'Authorization': f'sso-key {key}:{secret}',
        'Content-Type': 'application/json',
    }

    response = request("PUT", url, headers=headers, data=data)
    if response.status_code != 200:
        print(f"Something went wrong with domain {domain} subdomain {subdomain} when setting ip to {ip}."
              f" ERROR: {response.text}")


def main(args):
    if args.dev:
        import dotenv
        dotenv.load_dotenv()
    KEY = os.getenv("key")
    SECRET = os.getenv("secret")
    ip = get('https://api.ipify.org').text

    for domain, subdomain_list in zip(args.domain, args.subdomain):
        for subdomain in subdomain_list:
            update_domain(KEY, SECRET, ip, domain, subdomain)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Updates godaddy A record for domain with your external ip')
    parser.add_argument('--dev', action='store_true', help='Enable development mode.')
    parser.add_argument('-d', '--domain', action='append', required=True,
                        help='Domain name. Specify multiple times for multiple domains.')
    parser.add_argument('-s', '--subdomain', action='append', nargs='+', required=True,
                        help='List of subdomains for each domain. Specify after each domain.')

    args = parser.parse_args()

    if len(args.domain) != len(args.subdomain):
        parser.error("Each domain must have a corresponding list of subdomains.")
    main(args)
