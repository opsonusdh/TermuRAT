import time,sys
from subprocess import getoutput as output
from subprocess import run
import json
import requests

with open("data.json") as file:
    data = eval(file.read())
    token =  data["token"]
    

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


def download_image(url, save_path):
    response = requests.get(url)

    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
    else:
        return None

def visualize_data(data, indent=0, prefix='', count_st = 0):
    try:
        parsed = json.loads(str(data))
    except json.JSONDecodeError as e:
        print(data)
        return
        
    space = '    ' * indent

    if isinstance(parsed, dict):
        for key, value in parsed.items():
            if isinstance(value, (dict, list)):
                print(f"{space}\033[96m• {key}:\033[0m")
                visualize_json(value, indent + 1, prefix=key)
            else:
                print(f"{space}\033[95m{key}: \033[92m{value}\033[0m")

    elif isinstance(parsed, list):
        for i, item in enumerate(parsed, 1):
            if isinstance(item, dict):
                print(f"{space}\033[93m{count_st+i})\033[0m")
                for k, v in item.items():
                    if isinstance(v, (dict, list)):
                        print(f"{space}    \033[96m{k}:")
                        visualize_json(v, indent + 2)
                    else:
                        print(f"{space}    \033[95m{k}: \033[32m{v}\033[0m")
            elif isinstance(item, list):
                print(f"{space}\033[93m{count_st+i}.\033[0m (Nested list):")
                visualize_json(item, indent + 1)
            else:
                print(f"{space}\033[93m{count_st+i}) \033[92m{item}\033[0m")
    else:
        print(f"{space}\033[92m{data}\033[0m")
        
def save_data(data):
    with open("data.json", "w") as file:
        file.write(json.dumps(data))