import requests
import shutil
from tqdm.auto import tqdm
import os
import sys
from bs4 import BeautifulSoup
import re



def get_episode_link():
    FLAG = 0
    global pattern
    global a
    name = input("Enter TV Show/Movie Name: ")
    n_name = name.replace(' ', '+')
    s_url = f'https://ytstv.me/?s={n_name}'
    res = requests.get(s_url)
    if res.status_code != 200:
        print("Server Unreachable")
        sys.exit()
    soup = BeautifulSoup(res.content, 'html.parser')
    words = name.split()
    pattern = r"(?=.*\b" + r"\b)(?=.*\b".join(map(re.escape, words)) + r"\b)"
    if soup.h3.text == "No result found.":
        print(soup.h3.text)
        sys.exit()

    for link in soup.find_all('a'):
        match = re.search(pattern, str(link), flags=re.IGNORECASE)
        if match:
            print(link.get('href'))
            a = link.get('href')
            break
        else:
            pass
    print("Discovered download links: ")
    print('\n')
    res = requests.get(a)
    soup = BeautifulSoup(res.content, 'html.parser')
    pattern = r"(?=.*\b" + r"\b)(?=.*\b".join(map(re.escape, words)) + r"\b)"
    for link in soup.find_all('a'):
        match = re.search(pattern, str(link), flags=re.IGNORECASE)
        if match:
            # print(link.get('href'))
            a = link.get('href')
            x = a.replace(" ", "%20")
            if ".torrent" in x:
                print(x)
                FLAG = 1
            else:
                print(link.get('href'))
        else:
            pass
    if FLAG == True:
        sys.exit()


def resolution_link():
    print('\n')
    url = input("Copy and paste the above links to see different avaliable resolutions: ")
    print('\n')
    res = requests.get(url)
    soup = BeautifulSoup(res.content, 'html.parser')

    for link in soup.find_all('a'):
        match = re.search(pattern, str(link), flags=re.IGNORECASE)
        if match:
            a = link.get('href')
            x = a.replace(" ", "%20")
            if ".torrent" in x:
                print(x)
        else:
            pass
    print('\n')
    print("----------open .torrent links in browser or run download.py----------")

try:
    get_episode_link()
    resolution_link()
except KeyboardInterrupt:
    pass
