import os
import yaml
import json
import csv
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import filedialog, messagebox

RULES_PATH = "rules/suricata/rules.yaml"
OUTPUT_PATH = "output"

def load_rules():
    if not os.path.exists(RULES_PATH):
        messagebox.showerror("Error", f"No rules file found at {RULES_PATH}")
        return []
    with open(RULES_PATH, "r") as file:
        return yaml.safe_load(file)

def match_rules(lines, rules):
    alerts = []
    summary = {}
    for line in lines:
        for rule in rules:
            if rule["match"].lower() in line.lower():
                alerts.append({
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "line": line.strip()
                })
                summary[rule["name"]] = summary.get(rule["name"], 0) + 1
    return alerts, summary

def save_results(alerts, summary):
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    with open(os.path.join(OUTPUT_PATH, "alerts.json"), "w") as json_out:
        json.dump(alerts, json_out, indent=4)
    with open(os.path.join(OUTPUT_PATH, "alerts.csv"), "w", newline='') as csv_out:
        writer = csv.writer(csv_out)
        writer.writerow(["Rule Name", "Severity", "Match Count"])
        for rule, count in summary.items():
            severity = next((a["severity"] for a in alerts if a["rule_name"] == rule), "unknown")
            writer.writerow([rule, severity, count])

class SSIEMGUI:
    def __init__(self, root):
        root.title("Simple SIEM - Suricata Log Analyzer")
        root.geometry("800x600")
        root.resizable(False, False)

        self.file_path = ttk.StringVar()

        frame = ttk.Frame(root, padding=20)
        frame.pack(fill=BOTH, expand=True)

        ttk.Label(frame, text="📄 Suricata Log File", font=("Segoe UI", 12)).pack(anchor=W)
        ttk.Entry(frame, textvariable=self.file_path, width=80).pack(fill=X, pady=5)
        ttk.Button(frame, text="Browse", command=self.browse_file, bootstyle="info").pack(pady=5)

        ttk.Button(frame, text="🔍 Analyze Logs", command=self.analyze, bootstyle="success outline").pack(pady=10)

        self.output_text = ttk.Text(frame, wrap="word", font=("Consolas", 10))
        self.output_text.pack(expand=True, fill=BOTH)

    def browse_file(self):
        path = filedialog.askopenfilename(title="Select Suricata Log File")
        if path:
            self.file_path.set(path)

    def analyze(self):
        log_file = self.file_path.get()
        if not os.path.exists(log_file):
            messagebox.showerror("Error", "Log file not found.")
            return

        rules = load_rules()
        if not rules:
            return

        with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        alerts, summary = match_rules(lines, rules)

        self.output_text.delete(1.0, "end")
        self.output_text.insert("end", "=== ALERTS ===\n")
        for alert in alerts:
            self.output_text.insert("end", f"[{alert['severity'].upper()}] {alert['rule_name']} → {alert['line']}\n")

        self.output_text.insert("end", "\n=== SUMMARY ===\n")
        self.output_text.insert("end", f"Total log lines scanned: {len(lines)}\n")
        self.output_text.insert("end", f"Total alerts triggered : {len(alerts)}\n")
        for rule, count in summary.items():
            self.output_text.insert("end", f" - {rule}: {count} matches\n")

        save_results(alerts, summary)
        messagebox.showinfo("Done", "Analysis complete. Results saved to output/alerts.json and alerts.csv.")

if __name__ == "__main__":
    app = ttk.Window(themename="darkly")  # Try: flatly, darkly, cyborg, litera, etc.
    SSIEMGUI(app)
    app.mainloop()
