# 🔐 Caesar/XOR Cipher Tool (GUI)

A simple and intuitive PyQt5-based GUI application for encoding and decoding text using two classic ciphers: **Caesar** and **XOR**. Designed to showcase GUI development skills and basic cryptographic concepts, this tool is part of my cybersecurity Python portfolio.

---

## 🧰 Features

- 🧩 **Two cipher options**: Caesar Cipher and XOR Cipher
- 📑 **Two modes**: Encode and Decode (tab-based interface)
- ✍️ Input text field and key/shift entry
- 🖥️ Clean and responsive GUI built with **PyQt5**
- 📤 Instant display of encoded/decoded output

---

## 🖥️ How It Works

1. Launch the app (`python cipher_gui.py`)
2. Choose between **Encode** and **Decode** using the tabs
3. Select the cipher method: **Caesar** or **XOR**
4. Input the text and provide a:
   - 🔢 Caesar: integer shift (e.g. 3)
   - 🔐 XOR: string key (e.g. `secret`)
5. Click **Run** to see the result in real-time

---

## 🧪 Cipher Explanation

- **Caesar Cipher**: Shifts each letter in the text by a given number (e.g. `A` + 3 = `D`). Works only on alphabetic characters.
- **XOR Cipher**: Performs bitwise XOR between each character of the input and the key. Useful for basic obfuscation and reversible encoding.

---

## 🚀 Getting Started

### 📦 Requirements

- Python 3.6+
- `PyQt5`  
  Install with:
  ```bash
  pip install pyqt5
  ```

### ▶️ Run the App

```bash
python cipher_gui.py
```

---

## 🧠 Skills Demonstrated

- GUI programming with PyQt5
- Modular function design
- Handling text input/output
- Basic cryptography logic (Caesar, XOR)
- Event-driven UI updates

---

## 📁 Part of My Cybersecurity Python Projects

This project is part of my broader repository:  
🔗 [`Cybersecurity-Python-Projects`](https://github.com/your-username/Cybersecurity-Python-Projects)

---

## 📬 Feedback or Suggestions?

Feel free to open an issue or reach out — always open to collaboration or feedback!

