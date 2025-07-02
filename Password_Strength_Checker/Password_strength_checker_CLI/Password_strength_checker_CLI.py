import string
import math
import json

def get_pass():
    password = input("Enter your password: ")
    return password

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
    report= {
        "password": "*" * len(password),
        "score": score,
        "rating": rating
    }
    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

def run_code():
    password = get_pass()
    score, rating, tips = check_pass_strength(password)

    entropy = calculate_entropy(password)
    entropy_rating = rate_entropy(entropy)
    is_common = is_common_password(password)

    print(f"\nPassword strength: {rating} ({score}/5)")
    if tips:
        print("Suggestions:")
        for tip in tips:
            print(f" - {tip}")
    print(f"Entropy: {entropy:.2f} bits – {entropy_rating}")
    if is_common:
        print("Warning: This password is very common!")

    save_report(password, score, rating)

run_code()