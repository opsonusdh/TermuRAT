# TermuRAT

**TermuRAT** is a stealthy, terminal-based Android Remote Access Trojan (RAT) built for Termux. It uses private GitHub Gists as a command-and-control (C2) channel, allowing remote command execution and data exfiltration without direct connections or suspicious traffic.

## ⚙️ Features

- 🕵️ **Runs fully in Termux** – No need for Java, no app installs, just raw shell power.
- 🛰️ **Gist-based C2** – Pulls commands and uploads results via GitHub Gists.
- 🧠 **Timestamp logic** – Executes commands only when the Gist updates.
- 🧼 **Clean & Minimal** – Lightweight, no dependencies beyond Termux and `curl`.

## 🧠 How It Works

1. The Termux script checks a private GitHub Gist at intervals.
2. If the Gist has changed (timestamp/content), it fetches the new command.
3. The command is executed locally in Termux.
4. The output is pushed back to the same (or separate) Gist as response.

## 📁 Structure

- `termurat.sh` – Main RAT client script (runs on the target via Termux).
- `host.sh` – Control-side script to send commands and fetch results.

## 🚀 Setup

1. Create a **private GitHub Gist** for command and output.
2. Set your Gist ID and GitHub token in both scripts.
3. Run `termurat.sh` on the target device (via Termux).
4. Use `host.sh` to send commands and read results.

## 📦 Requirements

- Termux installed on target device
- GitHub account & token with Gist access
- 

## ⚠️ Disclaimer

> This tool is for **educational and ethical research purposes only**. Unauthorized access to devices or systems is illegal and unethical. You are responsible for how you use TermuRAT.

---

**Silent. Portable. Scripted.**
