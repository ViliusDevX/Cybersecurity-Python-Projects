# 🎣 Phishing URL Detector/Scanner

A Python GUI application that analyzes URLs for potential phishing threats by examining multiple security indicators including domain age, SSL certificates, URL structure, and more.

## 🔍 Features

- **🌐 Domain Age Analysis** — Checks domain registration date and flags newly registered domains
- **🔒 SSL Certificate Validation** — Verifies certificate validity and expiration
- **🔗 URL Structure Analysis** — Detects suspicious patterns and anomalies
- **📋 Blacklist Checking** — Simulated blacklist checks (extensible with real APIs)
- **📊 Content Analysis** — Simulated content inspection for phishing indicators
- **⚖️ Risk Scoring** — Calculates comprehensive risk percentage (0-100%)
- **💾 Export Functionality** — Saves detailed scan results to text files
- **🎨 Modern GUI** — Clean, dark-themed interface built with ttkbootstrap

## ⚙️ How It Works

1. **Enter a domain or URL** (e.g., `example.com` or `https://example.com/login`)
2. The application performs multiple security checks:
   - **Domain Age**: Analyzes registration date through WHOIS lookup
   - **SSL Certificate**: Validates certificate authenticity and expiration
   - **URL Structure**: Scans for suspicious patterns (IP addresses, hyphens, free TLDs)
   - **Blacklist Status**: Simulates blacklist checks (extensible to real APIs)
   - **Content Indicators**: Simulates content analysis for phishing signs
3. **Calculates a risk score** based on weighted factors from all checks
4. **Displays detailed results** with recommendations for further investigation

## 🧠 Risk Assessment System

| Risk Percentage | Verdict | Meaning |
|-----------------|---------|---------|
| 0-30% | ✅ Likely Safe | Minimal risk indicators detected |
| 31-60% | ⚠️ Suspicious | Some concerning elements present |
| 61-85% | 🚨 High Risk | Multiple phishing indicators detected |
| 86-100% | 🔴 Very High Risk | Strong evidence of phishing attempt |

## 🚦 Example URL Classifications

    ### High-Risk Indicators
    - `http://192.168.1.100/login.php` (IP address instead of domain)
    - `https://www.paypai.com/` (typosquatting - misspelled brand)
    - `https://apple.com.security-check.verify-user.com/` (deceptive subdomain)
    
    ### Medium-Risk Indicators
    - `https://secure-paypal.com/` (hyphenated brand name)
    - `https://chase-bank.xyz/` (unusual TLD with financial brand)
    - `https://bit.ly/3xAm9p2` (URL shortener - could mask destination)
    
    ### Low-Risk Examples
    - `https://www.paypal.com/login` (legitimate domain)
    - `https://accounts.google.com/signin` (authentic service)
    - `https://www.apple.com/account` (verified brand domain)

## 🛠️ Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/phishing-url-detector.git
cd phishing-url-detector

# Install dependencies
pip install -r requirements.txt

# Run the application
python phishing_scanner.py
```

### Requirements
    - Python 3.6+
    - ttkbootstrap
    - python-whois
    - requests

## 📋 Usage

    1. Launch the application
    2. Enter a URL to analyze in the input field
    3. Click "Scan URL" to begin analysis
    4. Review the detailed results showing all security checks
    5. Export results with the "Export Results" button if needed

---

⚠️ **Disclaimer**: 
This tool is intended for educational and research purposes only. 
It may occasionally give incomplete or inaccurate results. 
