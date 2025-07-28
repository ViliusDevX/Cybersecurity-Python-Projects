import requests
from http.cookies import SimpleCookie
from urllib.parse import urlparse
from datetime import datetime
from email.utils import parsedate_to_datetime
from collections import Counter

def audit_cookies(url):
    session = requests.Session()
    try:
        response = session.get(url, timeout=5, allow_redirects=False)
    except Exception as e:
        print(f"[X] Error fetching URL: {e}")
        return

    print(f"\n[+] Auditing cookies for: {url}\n")

    raw_cookie_header = response.headers.get('Set-Cookie', '')
    if not raw_cookie_header:
        print("No cookies found in response headers.")
        return

    parsed = SimpleCookie()
    parsed.load(raw_cookie_header)

    cookie_names = []
    insecure_count = 0
    summary = []

    for i, (name, morsel) in enumerate(parsed.items(), start=1):
        cookie_names.append(name)
        print(f"--- Cookie #{i} ---")
        print(f"Name     : {name}")
        print(f"Value    : {morsel.value}")

        flags = {
            "Secure": "secure" in morsel.keys(),
            "HttpOnly": "httponly" in morsel.keys(),
            "SameSite": "samesite" in morsel.keys()
        }

        for flag, present in flags.items():
            print(f"{flag:<10}: {'✔' if present else '✘'}")
            if not present:
                insecure_count += 1

        if "expires" in morsel:
            try:
                exp_date = parsedate_to_datetime(morsel["expires"])
                days_left = (exp_date - datetime.utcnow()).days
                print(f"Expires in : {days_left} days")
                if days_left > 365:
                    print("Note       : Long-lived cookie")
            except:
                print("Note       : Couldn't parse expiration date.")
        else:
            print("Note       : No expiry found (likely session cookie)")

        summary.append({
            "name": name,
            "secure": flags["Secure"],
            "httponly": flags["HttpOnly"],
            "samesite": flags["SameSite"]
        })

        print()

    duplicates = [item for item, count in Counter(cookie_names).items() if count > 1]
    if duplicates:
        print(f"Duplicate cookie names: {', '.join(duplicates)}\n")

    print("=== Summary ===")
    print(f"Cookies audited : {len(summary)}")
    print(f"Insecure flags  : {insecure_count}")
    print(f"Duplicates      : {len(duplicates)}")

    if insecure_count == 0:
        print("Security status : Strong")
    elif insecure_count <= len(summary):
        print("Security status : Moderate")
    else:
        print("Security status : Weak")

if __name__ == "__main__":
    print("Cookie Security Auditor")
    target = input("Enter URL (e.g., https://example.com): ").strip()

    parsed = urlparse(target)
    if not parsed.scheme.startswith("http"):
        print("Invalid URL. Please include http:// or https://")
    else:
        audit_cookies(target)
