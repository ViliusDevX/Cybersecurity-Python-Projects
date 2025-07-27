import tkinter as tk
from tkinter import scrolledtext, messagebox
import base64
import json
import jwt
from datetime import datetime
from jwt.exceptions import InvalidSignatureError, ExpiredSignatureError

def pad_b64(b64_string):
    return b64_string + '=' * (-len(b64_string) % 4)

def decode_jwt(token):
    try:
        header_b64, payload_b64, signature_b64 = token.split('.')
        header = json.loads(base64.urlsafe_b64decode(pad_b64(header_b64)).decode())
        payload = json.loads(base64.urlsafe_b64decode(pad_b64(payload_b64)).decode())
        return header, payload
    except Exception as e:
        messagebox.showerror("Decode Error", f"Failed to decode token:\n{e}")
        return None, None

def verify_signature(token, secret):
    try:
        jwt.decode(token, secret, algorithms=["HS256"])
        return True, "Signature is valid"
    except ExpiredSignatureError:
        return False, "Token has expired"
    except InvalidSignatureError:
        return False, "Invalid signature"
    except Exception as e:
        return False, f"Verification failed: {e}"

def check_exp(payload):
    if "exp" in payload:
        exp = datetime.utcfromtimestamp(payload["exp"])
        now = datetime.utcnow()
        if now > exp:
            return f"Token expired at: {exp} UTC"
        else:
            remaining = exp - now
            return f"Token expires at: {exp} UTC (in {remaining})"
    return "No 'exp' claim found"

def parse_token():
    token = token_input.get("1.0", tk.END).strip()
    secret = secret_input.get().strip()

    if not token:
        messagebox.showwarning("Input Error", "Please enter a JWT token.")
        return

    result_area.delete("1.0", tk.END)

    header, payload = decode_jwt(token)
    if header and payload:
        result_area.insert(tk.END, "=== JWT Header ===\n")
        result_area.insert(tk.END, json.dumps(header, indent=4) + "\n\n")

        result_area.insert(tk.END, "=== JWT Payload ===\n")
        result_area.insert(tk.END, json.dumps(payload, indent=4) + "\n\n")

        result_area.insert(tk.END, check_exp(payload) + "\n")

        if header.get("alg", "").lower() == "none":
            result_area.insert(tk.END, "Warning: The algorithm used is 'none', which is insecure.\n")

        if secret:
            valid, msg = verify_signature(token, secret)
            result_area.insert(tk.END, "\n=== Signature Verification ===\n" + msg + "\n")
        else:
            result_area.insert(tk.END, "\n(No secret provided — skipping signature verification)\n")

# GUI Setup
root = tk.Tk()
root.title("JWT Parser and Verifier")
root.geometry("700x600")

tk.Label(root, text="JWT Token:").pack()
token_input = scrolledtext.ScrolledText(root, height=6, width=80)
token_input.pack(pady=5)

tk.Label(root, text="Secret Key (optional for verifying HS256):").pack()
secret_input = tk.Entry(root, width=50, show="*")
secret_input.pack(pady=5)

parse_btn = tk.Button(root, text="Parse Token", command=parse_token, bg="#4CAF50", fg="white", height=2)
parse_btn.pack(pady=10)

tk.Label(root, text="Result:").pack()
result_area = scrolledtext.ScrolledText(root, height=20, width=80)
result_area.pack()

root.mainloop()
