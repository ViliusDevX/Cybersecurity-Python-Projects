# 🛡️ HTTP Header Analyzer (GUI)

A simple yet effective Python tool with a PyQt5 GUI to analyze HTTP response headers and check for common security header configurations. This is useful for web security testing, awareness, and educational purposes.

---

## 🚀 Features

- 🔎 Fetch HTTP headers from any website
- ✅ Displays HTTP status code and full response headers
- 🔐 Analyzes for important **security headers**, including:
  - `Strict-Transport-Security`
  - `Content-Security-Policy`
  - `X-Content-Type-Options`
  - `X-Frame-Options`
  - `X-XSS-Protection`
  - `Referrer-Policy`
  - `Permissions-Policy`
- 🖥️ Clean PyQt5-based GUI — no terminal needed

---

## 🧑‍💻 How It Works

1. Enter a full URL (e.g., `https://github.com`)
2. The app sends an HTTP GET request to the site
3. Headers are displayed in the app along with a status code
4. The tool checks for missing security headers and reports them

---

## 🛠️ Requirements

- Python 3.7+
- `PyQt5`
- `requests`

