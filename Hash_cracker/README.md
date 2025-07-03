# 🔓 Hash-Cracker

A simple Python tool to perform **dictionary-based hash cracking** using popular hashing algorithms (e.g., MD5, SHA-1, SHA-256). Includes a user-friendly GUI built with PyQt5.

## 🧠 What It Does

This tool performs **offline dictionary attacks** to identify plaintext values from hashed strings by:

1. Taking a target hash as input  
2. Trying each word in a wordlist (`rockyou.txt`)  
3. Hashing it using the selected algorithm  
4. Comparing it to the target  
5. Returning the original password if found  

It supports:
- MD5
- SHA-1
- SHA-256
- SHA-512
- SHA3-256, SHA3-512
- BLAKE2s, BLAKE2b  

## 🖥️ GUI Mode

Launch the tool with a simple graphical interface:
- Paste the hash you want to crack  
- Choose the hash type (or let the tool auto-detect based on length)  
- Provide a wordlist path (or leave blank to use `rockyou.txt`)  
- Click “Crack” and watch progress and results live  

You’ll see:
- Matching password (if found)  
- Time taken  
- Hash type used  
- Success/failure notification  

## 🧪 How It Works Internally

- Uses `hashlib` to compute the hash of each word  
- Auto-detects likely hash types based on input length  
- Uses PyQt5 for GUI interaction  
- Tracks time taken and allows flexible wordlist input  
- Defaults to using `rockyou.txt` if none is specified  

## ⚠️ About `rockyou.txt`

This tool uses the **rockyou.txt** wordlist, famous password list used in security research and CTFs.

However, it is **not included** in this repository because GitHub restricts bigger files.

## 🔽 How to Get `rockyou.txt`

Download the wordlist from this reliable source:

🔗 https://github.com/brannondorsey/naive-hashcat/releases/download/data/rockyou.txt

Place the file in the same directory as the script or point to it during runtime.

## 🧪 Example

```
Input Hash: 5f4dcc3b5aa765d61d8327deb882cf99
Detected Type: md5
Result: password
Time: 0.57 seconds
```

## 📚 Requirements

- Python 3.x  
- PyQt5  
- A wordlist (`rockyou.txt` or any custom one)

Install requirements with:
```bash
pip install pyqt5
```

## 🚀 Author

This tool is part of the **Cybersecurity-Python-Projects** series, a hands-on portfolio of practical tools created to refresh Python skills and explore real-world security concepts.

Built by an aspiring junior penetration tester & cybersecurity student.  
Suggestions, feedback, or contributions are always welcome — open an issue or reach out 🤙
