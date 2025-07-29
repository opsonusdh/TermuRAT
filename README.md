# TermuRAT

**TermuRAT** is a stealthy, terminal-based Android Remote Access Trojan (RAT) built for Termux. It uses private GitHub Gists as a command-and-control (C2) channel, allowing remote command execution and data exfiltration without direct connections or suspicious traffic.

## ⚙️ Features

- 🕵️ **Runs fully in Termux**
- 🛰️ **Gist-based C2** – Pulls commands and uploads results via GitHub Gists.
- 🧠 **Timestamp logic** – Executes commands only when the Gist updates.
- 🧼 **Clean & Minimal** – Lightweight, no dependencies beyond Termux and python in it.

## 🧠 How It Works

1. The Termux script checks a private GitHub Gist at intervals.
2. If the Gist has changed timestamp, it fetches the new command.
3. The command is executed locally in Termux in the target device.
4. The output is pushed back to another Gist as response.

## 📁 Structure

- `target.py` – Main RAT client script (runs on the target via Termux).
- `host.py` – Control-side script to send commands and fetch results.

## 🚀 Setup

1. Create a **GitHub Token**.
2. Set your GitHub token in host scripts.
3. Run `host.py`. It will genarate the gists and print in terminal.
4. Paste the token and gist id in target device and run `target.py` on target device via Termux.
5. Use `host.py` to send commands and read results.

## 📦 Requirements

- Termux and Termux:Api installed on target device.
- GitHub account & token with Gist access
- Terminal to send the command to target device.

## ⚠️ Disclaimer

This tool is for **educational and ethical research purposes only**. Unauthorized access to devices or systems is illegal and unethical. You are responsible for how you use TermuRAT.


