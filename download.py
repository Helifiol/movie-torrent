import requests
import shutil
from tqdm.auto import tqdm
import os



url = input("Enter Torrent link: ")

with requests.get(url, stream=True) as r:

    total_length = int(r.headers.get("Content-Length"))
    
    with tqdm.wrapattr(r.raw, "read", total=total_length, desc="Torrent File")as raw:
    
        with open(f"{os.path.basename(r.url)}", 'wb')as output:
            shutil.copyfileobj(raw, output)
