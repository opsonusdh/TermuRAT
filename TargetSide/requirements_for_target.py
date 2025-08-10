import time,sys,re
from subprocess import getoutput as output
from subprocess import run
import requests
import json

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
                "content": json.dumps(content)
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
        


colors = {
    # fundamental
    "newline": "\n",              # newline
    "tab": "\t",             # tab
    "clr": "\033[2J\033[H",  # clear screen & move cursor to top
    "bold": "\033[1m",       # bold text
    "dim": "\033[2m",        # dim text
    "italic": "\033[3m",     # italic text
    "underline": "\033[4m",  # underline
    "blink": "\033[5m",      # blink
    "reverse": "\033[7m",    # reverse colors
    "hidden": "\033[8m",     # hidden text
    "end": "\033[0m",
    
    # Regular text colors
    "black": "\033[30m",
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
    "white": "\033[37m",

    # Bold text colors
    "black_b": "\033[1;30m",
    "red_b": "\033[1;31m",
    "green_b": "\033[1;32m",
    "yellow_b": "\033[1;33m",
    "blue_b": "\033[1;34m",
    "magenta_b": "\033[1;35m",
    "cyan_b": "\033[1;36m",
    "white_b": "\033[1;37m",

    # Background colors
    "black_bg": "\033[40m",
    "red_bg": "\033[41m",
    "green_bg": "\033[42m",
    "yellow_bg": "\033[43m",
    "blue_bg": "\033[44m",
    "magenta_bg": "\033[45m",
    "cyan_bg": "\033[46m",
    "white_bg": "\033[47m",

    # Bright text colors (short names)
    "black_br": "\033[90m",
    "red_br": "\033[91m",
    "green_br": "\033[92m",
    "yellow_br": "\033[93m",
    "blue_br": "\033[94m",
    "magenta_br": "\033[95m",
    "cyan_br": "\033[96m",
    "white_br": "\033[97m",

    # Bright background colors (short names)
    "black_br_bg": "\033[100m",
    "red_br_bg": "\033[101m",
    "green_br_bg": "\033[102m",
    "yellow_br_bg": "\033[103m",
    "blue_br_bg": "\033[104m",
    "magenta_br_bg": "\033[105m",
    "cyan_br_bg": "\033[106m",
    "white_br_bg": "\033[107m",
}

def colorize(text):
    if text.startswith("\\"):
        return text[1:]

    def replace_code(match):
        code = match.group(1).strip()
        
        rgb_match = re.match(r"rgb\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", code)
        if rgb_match:
            r, g, b = map(int, rgb_match.groups())
            return f"\033[38;2;{r};{g};{b}m"

        rgb_bg_match = re.match(r"rgb_bg\((\d{1,3}),\s*(\d{1,3}),\s*(\d{1,3})\)", code)
        if rgb_bg_match:
            r, g, b = map(int, rgb_bg_match.groups())
            return f"\033[48;2;{r};{g};{b}m"

        return colors.get(code, f"{{{code}}}")

    return re.sub(r"\{(.*?)\}", replace_code, text)

