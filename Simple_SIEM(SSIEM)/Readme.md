# 🛡️ Simple SIEM (SSIEM) — GUI Suricata Log Analyzer

**SSIEM** is a lightweight, beginner-friendly SIEM-style tool designed to parse and analyze **Suricata** (or Snort-style) alerts using custom rule matching. 
It features a **modern graphical interface** built with `ttkbootstrap` and supports exporting alerts in JSON and CSV formats.

---

## 📦 Features

- ✅ GUI-based log analyzer (Tkinter + ttkbootstrap)
- 🔍 Custom rule-based log matching (defined in YAML)
- 📤 Exports alerts to CSV and JSON formats
- 💡 Modern UI with dark/light themes
- 🧪 Real-time detection of suspicious patterns
- 🗂️ Easy integration of Suricata text logs

---

## 📁 Project Structure

Simple_SIEM(SSIEM)/
├── SSIEM.py # Main GUI application
├── rules/
│ └── suricata/
│   └── rules.yaml # YAML rules for pattern detection
├── logs/ # Place your Suricata .txt log files here
├── output/ # Output folder for alerts.json & alerts.csv
└── README.md

---

## 🧠 Future Improvements

    📊 Threat scoring dashboards

    📂 Multiple log type support (auth, syslog, apache)

    📈 Graphical alert timelines

## ⚠️ Disclaimer

This tool is intended for educational and learning purposes only. Do not use SSIEM to analyze or store unauthorized log files. Always respect privacy and data security laws in your region.
