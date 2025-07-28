# 📄 Cookie Security Auditor

Browser_Cookie_Scanner is a Python-based tool that inspects the `Set-Cookie` headers from HTTP responses and evaluates the security of each cookie.

It checks for common best practices like `Secure`, `HttpOnly`, and `SameSite` flags, and gives a summary report with potential weaknesses.

---

## 🚀 Features

- Parses and displays all cookies from HTTP responses
- Checks for important security flags:
  - `Secure`
  - `HttpOnly`
  - `SameSite`
- Identifies session cookies (no expiration)
- Estimates cookie lifetime if `Expires` is present
- Detects duplicate cookie names
- Summarizes cookie security status at the end

---

## 🔒 What This Tool Does *Not* Do

    It does not send POST requests or login attempts

    It does not modify or steal cookies

    It does not run JavaScript (only inspects raw HTTP headers)

This tool is 100% passive and safe when used responsibly on public endpoints.

❗ Note: Most real websites only set cookies after login or via JavaScript, which this tool doesn’t see. Use known test endpoints to verify behavior.

## ⚠️ **Disclaimer**

This tool is intended for educational and ethical purposes only.

Do not use it to scan websites you do not own or have explicit permission to analyze.  
The author is not responsible for any misuse or legal issues caused by improper use of this tool.

Always follow responsible disclosure and respect the security policies of any target.
