import string
import math
import json
import tkinter as tk
from tkinter import messagebox

def is_common_password(password):
    with open("common_passwords.txt") as f:
        common = [line.strip() for line in f]
    return password.lower() in common

def calculate_entropy(password):
    charset = 0
    if any(c.islower() for c in password):
        charset += 26
    if any(c.isupper() for c in password):
        charset += 26
    if any(c.isdigit() for c in password):
        charset += 26
    if any(c in string.punctuation for c in password):
        charset += len(string.punctuation)
    entropy = len(password) * math.log2(charset) if charset else 0
    return entropy

def rate_entropy(entropy):
    if entropy < 28:
        return "Crackable in seconds."
    elif entropy < 36:
        return "Fair, but not strong."
    elif entropy < 60:
        return "Strong."
    else:
        return "Very strong."

def analyze_password_components(password):
    score = 0
    tips = []

    if any(c.islower() for c in password):
        score += 1
    else:
        tips.append("Tip: Add lowercase letters.")
    if any(c.isupper() for c in password):
        score += 1
    else:
        tips.append("Tip: Add uppercase letters.")
    if any(c.isdigit() for c in password):
        score += 1
    else:
        tips.append("Tip: Add digits.")
    if any(c in string.punctuation for c in password):
        score += 1
    else:
        tips.append("Tip: Add symbols.")
    if len(password) >= 12:
        score += 1
    else:
        tips.append("Tip: Make it at least 12 characters long.")

    return score, tips

def rate_password(score):
    if score <= 2:
        return "Weak"
    elif score == 3:
        return "Medium"
    elif score == 4:
        return "Strong"
    else:
        return "Very Strong"

def check_pass_strength(password):
    score, tips = analyze_password_components(password)
    rating = rate_password(score)
    return score, rating, tips

def save_report(password, score, rating):
    report = {
        "password": "*" * len(password),
        "score": score,
        "rating": rating
    }
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

# -------------------- GUI --------------------

def check_password_gui():
    password = entry.get()
    if not password:
        messagebox.showwarning("Input Error", "Please enter a password.")
        return

    score, rating, tips = check_pass_strength(password)
    entropy = calculate_entropy(password)
    entropy_rating = rate_entropy(entropy)
    is_common = is_common_password(password)

    save_report(password, score, rating)

    result = f"Password strength: {rating} ({score}/5)\n"
    result += f"Entropy: {entropy:.2f} bits – {entropy_rating}\n"
    if is_common:
        result += "\n⚠️ Warning: This password is very common!\n"
    if tips:
        result += "\nSuggestions:\n" + "\n".join(f" - {tip}" for tip in tips)

    messagebox.showinfo("Password Analysis", result)

# Build GUI
root = tk.Tk()
root.title("Password Strength Checker")
root.geometry("400x200")

label = tk.Label(root, text="Enter your password:")
label.pack(pady=10)

entry = tk.Entry(root, show="*", width=30)
entry.pack()

btn = tk.Button(root, text="Check Password", command=check_password_gui)
btn.pack(pady=10)

root.mainloop()
