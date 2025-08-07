import tkinter as tk
from tkinter import scrolledtext, messagebox
import requests
from urllib.parse import urlparse, urlencode, urlunparse, parse_qs

payloads = [
    "https://evil.com",
    "//evil.com",
    "/\\evil.com",
    "http://evil.com@target.com"
]

def test_url_for_redirect(base_url, param):
    results = []
    for payload in payloads:
        parsed = urlparse(base_url)
        qs = parse_qs(parsed.query)
        qs[param] = payload
        new_query = urlencode(qs, doseq=True)
        test_url = urlunparse(parsed._replace(query=new_query))

        try:
            resp = requests.get(test_url, allow_redirects=False, timeout=5)
            if 300 <= resp.status_code < 400 and 'Location' in resp.headers:
                location = resp.headers['Location']
                if 'evil.com' in location:
                    results.append(f"[!] POSSIBLE OPEN REDIRECT:\n{test_url} ➡ {location}\n")
                else:
                    results.append(f"[-] Redirects elsewhere:\n{test_url} ➡ {location}\n")
            else:
                results.append(f"[+] No redirect for: {test_url}\n")
        except Exception as e:
            results.append(f"[!] Error testing {test_url}: {str(e)}\n")
    return results

def start_scan():
    urls = url_input.get("1.0", tk.END).strip().splitlines()
    param = param_input.get().strip()

    if not urls or not param:
        messagebox.showerror("Input Error", "Please enter URL(s) and a parameter name.")
        return

    result_output.delete("1.0", tk.END)
    for url in urls:
        result_output.insert(tk.END, f"\n=== Testing URL: {url} ===\n")
        results = test_url_for_redirect(url.strip(), param)
        for line in results:
            result_output.insert(tk.END, line)

root = tk.Tk()
root.title("Open Redirect Scanner")

tk.Label(root, text="Enter URL(s):").pack()
url_input = scrolledtext.ScrolledText(root, height=5, width=80)
url_input.pack(pady=5)

tk.Label(root, text="Redirect parameter (e.g., 'url', 'redirect')").pack()
param_input = tk.Entry(root, width=50)
param_input.pack(pady=5)

tk.Button(root, text="Scan", command=start_scan).pack(pady=10)

tk.Label(root, text="Results:").pack()
result_output = scrolledtext.ScrolledText(root, height=15, width=100)
result_output.pack(pady=5)

root.mainloop()