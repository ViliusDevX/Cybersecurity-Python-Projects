# 🛡️ Simple SIEM (SSIEM) — GUI-Based Log Analyzer

SSIEM is a lightweight, beginner-friendly security log analyzer designed to parse and analyze log files using customizable YAML rule matching.
It supports both Suricata text logs and DNS JSON logs with a modern GUI built using ttkbootstrap.

## 📦 Features

    ✅ Modern GUI with theme support (built using Tkinter + ttkbootstrap)

    🧩 Suricata .txt and DNS .json log parsing

    🧠 Flexible, custom rule matching via simple rules.yaml

    🧪 Automatically detects patterns and flags alerts with severity

    📤 Exports results to alerts.csv and alerts.json

    🔢 Includes line number reference for each alert

    📁 Clean, modular folder structure for easy management

## 🗂️ Supported Log Types

Log Type	Format	Description
Suricata	.txt	Snort-style IDS logs in plaintext
DNS	.json	JSON logs exported from tools like tshark or Wireshark

## 📁 Project Structure

    Simple_SIEM(SSIEM)/
    ├── SSIEM.py                   # Main GUI application
    ├── rules/
    │   ├── suricata/
    │   │   └── rules.yaml         # Suricata log rules
    │   └── dns/
    │       └── rules.yaml         # DNS log rules
    ├── logs/                      # Place your log files here (Suricata .txt or DNS .json)
    ├── output/                    # Alert results exported here (CSV + JSON)
    └── README.md                  # This file

## 🛠️ How to Use

    Launch SSIEM.py

    Choose log type: Suricata or DNS

    Browse and select a log file (.txt or .json)

    Click "Analyze"

    View alerts and summary, then check output/alerts.csv and alerts.json for results

## 🔮 Planned Enhancements

    📊 Threat scoring and severity-based charts

    📈 Interactive timeline of detected events

    🧱 More built-in rule templates (for syslog, auth, Apache, etc.)

    💬 Regex support and metadata-based matching

    ☁️ Cloud-based log ingestion support

## ⚠️ Disclaimer

    This tool is intended strictly for educational and research purposes. Do not use SSIEM to analyze logs from unauthorized systems. Always follow data protection and privacy laws applicable in your jurisdiction.
