# 🔀 Simple Redirect Scanner (GUI)

A lightweight Python tool with a simple GUI to detect potential **open redirect vulnerabilities** in URLs. 
Designed for security testing, this scanner analyzes how web applications handle redirect parameters and identifies unsafe behavior.

---

## 🎯 Features

- ✅ Tests for common open redirect payloads (e.g. `https://evil.com`, `//evil.com`, etc.)
- ✅ Easy-to-use GUI built with Tkinter
- ✅ Highlights potentially vulnerable redirect behavior
- ✅ Supports scanning multiple URLs at once
- ✅ Displays full HTTP redirect target and status

---

## 🧪 How to Use

  Paste one or more URLs in the "Enter URL(s)" box
  Example:

  https://example.com/redirect?url=https://google.com

  Enter the redirect parameter name (e.g., url, redirect, next)

  Click Scan

  View results in the output box:

    [+] → Not vulnerable
  
    [!] → Possibly vulnerable
  
    Redirect chain and target shown for each test

## ⚙️ How It Works

The tool sends requests with known open redirect payloads, such as:

    https://evil.com

    //evil.com

    /\evil.com

    http://evil.com@target.com

It checks for:

    3xx status codes

    Location headers pointing to external domains

If the server redirects users to the supplied value without validation, it's likely vulnerable to an open redirect attack.

## ⚠️ Disclaimer

This tool is intended for educational and authorized testing only.
Do not scan third-party systems without proper permission.
