# 🌐 simple_ip_info_checker

A lightweight Python + PyQt5 desktop tool that retrieves useful metadata about any IP address using public IP lookup APIs. Designed for students, analysts, and developers who need quick IP context without reputation scoring or authentication tokens.

---

## 🚀 Features

- Fetches basic information about an IP:
  - 🌍 Country, region, and city
  - 🏢 ISP and ASN
  - 📌 Coordinates (latitude/longitude)
  - 🕒 Timezone
  - 🔒 Proxy/VPN detection (basic)
- Uses public APIs (`ip-api.com`, `ipwho.is`) with **no API key needed**
- Modern GUI built using **PyQt5**
- Fast and offline-friendly fallback logic between APIs

---

## 🧰 Requirements

- Python 3.x
- PyQt5
- requests

pip install PyQt5 requests

## 📦 Usage

- python simple_ip_info_checker.py


## 📘 Notes

    This tool is not an IP reputation checker. It simply shows metadata about the IP address.

    It may be used to assist in general OSINT, basic forensics, or cybersecurity scripting.
