# 🔐 TLS Certificate Analyzer

A simple Python tool that retrieves and analyzes the TLS/SSL certificate of a given domain. 
Useful for checking certificate validity, issuer information, and expiration.

---

## 🎯 Features

- Connects to any HTTPS domain
- Retrieves certificate details:
  - Issued to (Common Name)
  - Issued by (Certificate Authority)
  - Validity period (start & end)
  - Days left until expiration
  - Status: valid or expired
- CLI-based with user-friendly prompts
- Uses only Python standard libraries

---

## 🚀 Usage

📁 File Structure

TLS_analyzer/
│
├── analyzer.py       # Main Python script
└── README.md         # Project documentation


🛡️ Disclaimer

This tool is intended for educational and informational purposes only. 
Always ensure you have permission to scan or inspect services.
