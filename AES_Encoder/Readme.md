# 🔐 AES Encryption/Decryption Tool (CBC Mode)

A lightweight GUI-based tool for AES encryption and decryption using the secure CBC (Cipher Block Chaining) mode. Designed for learning, local data security, and demonstrating how symmetric encryption works.

## 🎯 Features

  🧠 Beginner-friendly GUI using ttkbootstrap

  🔐 AES-128/192/256 encryption in CBC mode

  ✍️ User-provided plaintext and keys

  🔁 Real-time Encrypt / Decrypt toggling

  🧊 Random IV (Initialization Vector) generation

  📋 Copyable encrypted & decrypted text

## 🧠 Concepts Used

  Concept	Description
  AES (CBC mode)	A secure block cipher algorithm
  Key	Secret used for both encryption and decryption (must be 16, 24, or 32 bytes)
  IV (Initialization Vector)	Random 16-byte string to make each encryption unique
  Padding	Fills data to a multiple of 16 bytes, required by AES
  
## 📁 Project Structure

    AES_CBC_Tool/
    ├── aes_gui.py          # Main GUI script
    ├── requirements.txt    # Dependencies
    └── README.md

## ⚠️ Disclaimer

    This tool is for educational and learning purposes only.
