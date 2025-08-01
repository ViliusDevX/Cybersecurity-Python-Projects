import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import base64

def pad(text):
    pad_len = 16 - (len(text) % 16)
    return text + chr(pad_len) * pad_len

def unpad (text):
    return text[:-ord(text[-1])]

def encrypt(text, key):
    key = key.ljust(16)[:16].encode()
    iv = get_random_bytes(16)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_text = pad(text).encode()
    encrypted = cipher.encrypt(padded_text)
    return base64.b64encode(iv + encrypted).decode()

def decrypt(ciphertext, key):
    try:
        key = key.ljust(16)[:16].encode()
        raw = base64.b64decode(ciphertext)
        iv = raw[:16]
        encrypted = raw[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = cipher.decrypt(encrypted)
        return unpad(decrypted.decode())
    except Exception as e:
        return f"[Error] {str(e)}"

def do_encrypt():
    msg = input_text.get("1.0", "end").strip()
    key = key_entry.get().strip()
    if not msg or not key:
        output_text.delete("1.0", "end")
        output_text.insert("1.0", "⚠️ Input text and key are required.")
        return
    encrypted = encrypt(msg, key)
    output_text.delete("1.0", "end")
    output_text.insert("1.0", encrypted)


def do_decrypt():
    msg = input_text.get("1.0", "end").strip()
    key = key_entry.get().strip()
    if not msg or not key:
        output_text.delete("1.0", "end")
        output_text.delete("1.0", "⚠️ Encrypted text and key are required.")
        return
    decrypted = decrypt(msg, key)
    output_text.delete("1.0", "end")
    output_text.insert("1.0", decrypted)

app = ttk.Window(title="AES CBC Encryptor/Decryptor", themename="superhero", size=(700, 550))

ttk.Label(app, text="🔐 AES Encryption Key (max 16 characters):", font=("Segoe UI", 11)).pack(pady=10)
key_entry = ttk.Entry(app, width=40, font=("Segoe UI", 11))
key_entry.pack(pady=5)

ttk.Label(app, text="✍️ Input Text / Encrypted Text:", font=("Segoe UI", 11)).pack(pady=(15, 5))
input_text = ttk.Text(app, height=6, font=("Consolas", 10))
input_text.pack(padx=10, fill=BOTH, expand=True)

btn_frame = ttk.Frame(app)
btn_frame.pack(pady=10)
ttk.Button(btn_frame, text="🔒 Encrypt", command=do_encrypt, bootstyle=SUCCESS).pack(side=LEFT, padx=10)
ttk.Button(btn_frame, text="🔓 Decrypt", command=do_decrypt, bootstyle=PRIMARY).pack(side=LEFT, padx=10)

ttk.Label(app, text="📤 Output:", font=("Segoe UI", 11)).pack(pady=5)
output_text = ttk.Text(app, height=6, font=("Consolas", 10))
output_text.pack(padx=10, fill=BOTH, expand=True)

app.mainloop()