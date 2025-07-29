import time,sys
from subprocess import getoutput as output
from subprocess import run
import requests

with open("data.json") as file:
    data = eval(file.read())
    token =  data["token"]

if not data["token"] or not data["to_target_gist_id"] or not data["to_host_gist_id"]:
    print("Initial data not givwn by user in the data.json file. Aborting...")
    sys.exit()

def edit_gist(gist_id, filename, content):
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    payload = {
        "files": {
            filename: {
                "content": content
            }
        }
    }
    response = requests.patch(f"https://api.github.com/gists/{gist_id}", headers=headers, json=payload)

    if response.status_code == 200:
        return True
    else:
        raise ConnectionError(response.text)


def create_gist(filename, content):
    payload = {
        "public": False,
        "files": {
             filename: {
            "content": json.dumps(content)
        }
    }
}
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.post("https://api.github.com/gists",headers=headers, json=payload)
    
    if response.status_code == 201:
        gist_url = response.json()['html_url']
        return gist_url
    else:
        raise ConnectionError(response.text)
        
        
def read_gist(gist_id):
    url = f"https://api.github.com/gists/{gist_id}"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        gist_data = response.json()
        for filename, file_info in gist_data["files"].items():
            return (file_info["content"]) 
    else:
        raise ConnectionError(response.text)


def upload_image(image_path):
    headers = {
        "User-Agent": "curl/7.68.0"
    }
    with open(image_path, 'rb') as f:
        response = requests.post('https://0x0.st', files={'file': f}, headers=headers)

    if response.status_code == 200:
        return response.text.strip()
    else:
        return None


def save_data(data):
    with open("data.json", "w") as file:
        file.write(json.dumps(data))
        
