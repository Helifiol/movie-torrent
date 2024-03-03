import requests
import shutil
from tqdm.auto import tqdm
import os
import sys
from bs4 import BeautifulSoup
import re

print("""
▒█▀▄▀█ █▀▀█ ▀█░█▀ ░▀░ █▀▀ 　 ▀▀█▀▀ █▀▀█ █▀▀█ █▀▀█ █▀▀ █▀▀▄ ▀▀█▀▀ 
▒█▒█▒█ █░░█ ░█▄█░ ▀█▀ █▀▀ 　 ░▒█░░ █░░█ █▄▄▀ █▄▄▀ █▀▀ █░░█ ░░█░░ 
▒█░░▒█ ▀▀▀▀ ░░▀░░ ▀▀▀ ▀▀▀ 　 ░▒█░░ ▀▀▀▀ ▀░▀▀ ▀░▀▀ ▀▀▀ ▀░░▀ ░░▀░░""")

episode_numbers = {}

def get_episode_link():
    try:
        FLAG = 0
        global episode_numbers
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
        count = 0
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
                    # print(link.get('href'))
                    episode_numbers[count] = link.get('href')
                    count = count + 1
                    # pass
            else:
                pass
        for key, value in episode_numbers.items():
            print(key, ':', value)

        if FLAG == True:
            sys.exit()
    except Exception as err:
        print("An error occured " ,err)


def resolution_link():
    try:
        res_links = {}
        print('\n')
        # url = input("Copy and paste the above links to see different avaliable resolutions: ")
        number = int(input("enter link number: "))
        url = episode_numbers.get(number)
        print(url)
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        count = 0

        for link in soup.find_all('a'):
            match = re.search(pattern, str(link), flags=re.IGNORECASE)
            if match:
                a = link.get('href')
                x = a.replace(" ", "%20")
                if ".torrent" in x:
                    # print(x)
                    res_links[count] = x
                    count = count + 1
            else:
                pass
        print('\n')
        for key, val in res_links.items():
            print(key, ":", val)
        if len(res_links) == 0:
            print("No links found")
        else:
            link_down_url = res_links.get(int(input("Enter link number to be dowloaded: ")))
            download(link_down_url)
    except Exception as err:
        print("An error occured " ,err)


def download(link_url):
    url = link_url

    with requests.get(url, stream=True) as r:

        total_length = int(r.headers.get("Content-Length"))
        
        with tqdm.wrapattr(r.raw, "read", total=total_length, desc="Torrent File")as raw:
        
            with open(f"{os.path.basename(r.url)}", 'wb')as output:
                shutil.copyfileobj(raw, output)


try:
    while True:
        get_episode_link()
        resolution_link()
        response = str(input("Download another: y/n :"))
        if response.lower() == 'n':
            print("Goodbye")
            break
except Exception as err:
    print(err)
