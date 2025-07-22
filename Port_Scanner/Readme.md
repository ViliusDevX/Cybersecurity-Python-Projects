# 🔍 Simple Python Port Scanner

This is a lightweight GUI-based port scanner built with Python. It allows you to scan a domain or IP address over a selected port range and displays banners (if available) to help identify running services.

##  Features

- Scan any IP or domain
- Set custom port range
- Multi-threaded for faster scanning
- Basic service banner detection
- GUI interface using PyQt5

## Example Output

Scanning scanme.nmap.org from port 20 to 100...

✅ Port 22 is open (SSH-2.0-OpenSSH_6.6.1p1 Ubuntu-2ubuntu2.13)

✅ Port 80 is open (HTTP/1.1 400 Bad Request)

✅ Port 135 is open (⚠️ Open (no response))


## ⚠️ Disclaimer

This tool is intended only for educational and learning use.
Do not scan domains or networks you don't own or have permission to test.
Banner detection may give incomplete or no results depending on service response.

    ❗ Unauthorized scanning may be illegal in your country. Use responsibly.
