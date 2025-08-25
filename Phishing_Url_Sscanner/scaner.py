import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import socket
import whois
import ssl
import datetime
import requests
import re
from urllib.parse import urlparse
import json
import time
from concurrent.futures import ThreadPoolExecutor
import threading

class PhishingURLScanner:
    def __init__(self):
        self.root = ttk.Window(themename="darkly")
        self.root.title("Phishing URL Scanner")
        self.root.geometry("900x700")

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(2, weight=1)

        self.create_widgets()
        self.scanning = False

    def create_widgets(self):
        header = ttk.Label(self.root, text="Phishing URL Scanner",
                           font=("Helvetica", 16, "bold"))
        header.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        input_frame = ttk.Frame(self.root)
        input_frame.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        input_frame.grid_columnconfigure(1, weight=1)

        ttk.Label(input_frame, text="URL to scan:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.url_entry = ttk.Entry(input_frame, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.scan_btn = ttk.Button(input_frame, text="Scan URL",
                                   command=self.start_scan, bootstyle=PRIMARY)
        self.scan_btn.grid(row=0, column=2, padx=5, pady=5)

        self.progress = ttk.Progressbar(self.root, mode='indeterminate')
        self.progress.grid(row=2, column=0, padx=10, pady=5, sticky="ew")

        results_frame = ttk.LabelFrame(self.root, text="Scan Results")
        results_frame.grid(row=3, column=0, padx=10, pady=10, sticky="nsew")
        results_frame.grid_columnconfigure(0, weight=1)
        results_frame.grid_rowconfigure(0, weight=1)

        self.results_text = scrolledtext.ScrolledText(results_frame, height=20, wrap=tk.WORD)
        self.results_text.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        risk_frame = ttk.Frame(self.root)
        risk_frame.grid(row=4, column=0, padx=10, pady=5, sticky="ew")

        ttk.Label(risk_frame, text="Risk Score:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.risk_var = tk.StringVar(value="Not scanned")
        risk_label = ttk.Label(risk_frame, textvariable=self.risk_var, font=("Helvetica", 14, "bold"))
        risk_label.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        buttons_frame = ttk.Frame(self.root)
        buttons_frame.grid(row=5, column=0, padx=10, pady=10)

        self.export_btn = ttk.Button(buttons_frame, text="Export Results",
                                     command=self.export_results, bootstyle=INFO, state="disabled")
        self.export_btn.pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="Clear",
                   command=self.clear_results, bootstyle=WARNING).pack(side=tk.LEFT, padx=5)

        ttk.Button(buttons_frame, text="Exit",
                   command=self.root.quit, bootstyle=DANGER).pack(side=tk.LEFT, padx=5)

    def start_scan(self):
        if self.scanning:
            return

        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Please enter a URL to scan.")
            return

        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        self.scanning = True
        self.scan_btn.config(state="disabled")
        self.progress.start(10)
        self.results_text.delete("1.0", tk.END)
        self.results_text.insert(tk.END, f"Scanning URL: {url}...\n")
        self.results_text.insert(tk.END, "-" * 50 + "\n")

        threading.Thread(target=self.scan_url, args=(url,), daemon=True).start()

    def scan_url(self, url):
        try:
            results = {}
            risk_score = 0
            max_score = 0

            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            domain_age_result = self.check_domain_age(domain)
            results["Domain Age"] = domain_age_result
            risk_score += domain_age_result["score"]
            max_score += domain_age_result["max_score"]

            ssl_result = self.check_ssl_certificate(domain)
            results["SSL Certificate"] = ssl_result
            risk_score += ssl_result["score"]
            max_score += ssl_result["max_score"]

            url_struct_result = self.check_url_structure(url)
            results["URL Structure"] = url_struct_result
            risk_score += url_struct_result["score"]
            max_score += url_struct_result["max_score"]

            blacklist_result = self.check_blacklists(domain)
            results["Blacklist"] = blacklist_result
            risk_score += blacklist_result["score"]
            max_score += blacklist_result["max_score"]

            content_result = self.check_content(url)
            results["Content Analysis"] = content_result
            risk_score += content_result["score"]
            max_score += content_result["max_score"]

            risk_percentage = (risk_score / max_score) * 100 if max_score > 0 else 0

            self.root.after(0, self.display_results, results, risk_percentage)

        except Exception as e:
            self.root.after(0, self.scan_error, str(e))
        finally:
            self.root.after(0, self.scan_complete)

    def check_domain_age(self, domain):
        result = {
            "status": "Unknown",
            "details": "",
            "score": 5,
            "max_score": 5
        }

        try:
            domain_info = whois.whois(domain)
            if domain_info.creation_date:
                if isinstance(domain_info.creation_date, list):
                    domain_creation_date = domain_info.creation_date[0]
                else:
                    domain_creation_date = domain_info.creation_date

                domain_age = (datetime.datetime.now() - domain_creation_date).days

                if domain_age < 30:
                    result["status"] = "High Risk"
                    result["details"] = f"Domain is very new ({domain_age} days old)"
                    result["score"] = 5
                elif domain_age < 365:
                    result["status"] = "Medium Risk"
                    result["details"] = f"Domain is relatively new ({domain_age} days old)"
                    result["score"] = 3
                else:
                    result["status"] = "Low Risk"
                    result["details"] = f"Domain is established ({domain_age} days old)"
                    result["score"] = 0
            else:
                result["details"] = "Could not retrieve domain creation date"

        except Exception as e:
            result["details"] = f"Error checking domain age: {str(e)}"

        return result

    def check_ssl_certificate(self, domain):
        """Check SSL certificate validity"""
        result = {
            "status": "Unknown",
            "details": "",
            "score": 5,  # Default risk score for unknown
            "max_score": 5
        }

        try:
            context = ssl.create_default_context()
            with socket.create_connection((domain, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=domain) as ssock:
                    cert = ssock.getpeercert()

                    # Check certificate expiration
                    exp_date = datetime.datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
                    days_until_exp = (exp_date - datetime.datetime.now()).days

                    if days_until_exp < 7:
                        result["status"] = "High Risk"
                        result["details"] = f"SSL certificate expires in {days_until_exp} days"
                        result["score"] = 5
                    elif days_until_exp < 30:
                        result["status"] = "Medium Risk"
                        result["details"] = f"SSL certificate expires in {days_until_exp} days"
                        result["score"] = 3
                    else:
                        result["status"] = "Low Risk"
                        result["details"] = f"SSL certificate valid for {days_until_exp} days"
                        result["score"] = 0
        except Exception as e:
            result["status"] = "High Risk"
            result["details"] = f"No valid SSL certificate: {str(e)}"
            result["score"] = 5

        return result

    def check_url_structure(self, url):
        """Analyze URL structure for suspicious patterns"""
        result = {
            "status": "Analyzing",
            "details": "",
            "score": 0,
            "max_score": 15
        }

        suspicious_patterns = [
            (r'\d+\.\d+\.\d+\.\d+', 5, "IP address in domain name"),
            (r'@', 5, "Contains '@' character (possible credential embedding)"),
            (r'-', 2, "Hyphens in domain (often used in phishing)"),
            (r'\.(tk|ml|ga|cf|gq)$', 5, "Free domain extension (higher risk)"),
            (r'(login|signin|account|verify|secure)\.?[^/]*$', 3, "Suspicious keywords in domain"),
            (r'https?://[^/]+/.*[&=]http', 4, "Potential redirect to external site"),
        ]

        details = []
        total_score = 0

        for pattern, score, description in suspicious_patterns:
            if re.search(pattern, url, re.IGNORECASE):
                details.append(description)
                total_score += score

        if total_score == 0:
            result["status"] = "Low Risk"
            result["details"] = "No suspicious URL patterns detected"
        elif total_score < 5:
            result["status"] = "Medium Risk"
            result["details"] = "Some suspicious patterns: " + "; ".join(details)
        else:
            result["status"] = "High Risk"
            result["details"] = "Multiple suspicious patterns: " + "; ".join(details)

        result["score"] = total_score
        return result

    def check_blacklists(self, domain):
        """Check domain against blacklists (simulated)"""
        result = {
            "status": "Simulated Check",
            "details": "This is a simulation. Real implementation would check multiple blacklists.",
            "score": 0,
            "max_score": 10
        }

        # Simulate blacklist check with random results for demonstration
        import random
        if random.random() < 0.2:  # 20% chance of being "blacklisted"
            result["status"] = "High Risk"
            result["details"] = "Domain found in simulated blacklist"
            result["score"] = 10
        else:
            result["status"] = "Low Risk"
            result["details"] = "Domain not found in simulated blacklists"

        return result

    def check_content(self, url):
        """Analyze page content for phishing indicators (simulated)"""
        result = {
            "status": "Simulated Check",
            "details": "This is a simulation. Real implementation would fetch and analyze page content.",
            "score": 0,
            "max_score": 10
        }

        # Simulate content analysis with random results for demonstration
        import random
        risk_score = random.randint(0, 10)

        if risk_score > 7:
            result["status"] = "High Risk"
            result["details"] = "Simulated detection of phishing content (login forms, brand impersonation)"
            result["score"] = risk_score
        elif risk_score > 3:
            result["status"] = "Medium Risk"
            result["details"] = "Simulated detection of some suspicious content elements"
            result["score"] = risk_score
        else:
            result["status"] = "Low Risk"
            result["details"] = "No obvious phishing content detected in simulation"

        return result

    def display_results(self, results, risk_percentage):
        """Display scan results in the GUI"""
        self.results_text.delete(1.0, tk.END)

        url = self.url_entry.get().strip()
        self.results_text.insert(tk.END, f"Scan Results for: {url}\n")
        self.results_text.insert(tk.END, "=" * 50 + "\n\n")

        for check_name, result in results.items():
            self.results_text.insert(tk.END, f"{check_name}:\n")
            self.results_text.insert(tk.END, f"  Status: {result['status']}\n")
            self.results_text.insert(tk.END, f"  Details: {result['details']}\n")
            self.results_text.insert(tk.END, f"  Risk Score: {result['score']}/{result['max_score']}\n")
            self.results_text.insert(tk.END, "-" * 30 + "\n")

        self.results_text.insert(tk.END, f"\nOverall Risk: {risk_percentage:.1f}%\n")

        # Set risk color based on percentage
        if risk_percentage > 70:
            risk_color = "red"
        elif risk_percentage > 40:
            risk_color = "orange"
        else:
            risk_color = "green"

        self.risk_var.set(f"{risk_percentage:.1f}%")

        # Enable export button
        self.export_btn.config(state="normal")

    def scan_error(self, error_msg):
        """Handle scan errors"""
        self.results_text.insert(tk.END, f"\nError during scan: {error_msg}\n")
        self.risk_var.set("Error")

    def scan_complete(self):
        """Clean up after scan completion"""
        self.scanning = False
        self.scan_btn.config(state="normal")
        self.progress.stop()

    def export_results(self):
        """Export results to a JSON file"""
        try:
            # Get the results text
            results_text = self.results_text.get(1.0, tk.END)

            # Create a filename with timestamp
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            url = self.url_entry.get().strip()[:50]  # Limit filename length
            safe_url = "".join(c for c in url if c.isalnum() or c in ('-', '_')).rstrip()
            filename = f"phishing_scan_{safe_url}_{timestamp}.txt"

            # Write to file
            with open(filename, 'w') as f:
                f.write(results_text)

            messagebox.showinfo("Export Successful", f"Results exported to {filename}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export results: {str(e)}")

    def clear_results(self):
        """Clear the results area"""
        self.results_text.delete(1.0, tk.END)
        self.risk_var.set("Not scanned")
        self.export_btn.config(state="disabled")

    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PhishingURLScanner()
    app.run()