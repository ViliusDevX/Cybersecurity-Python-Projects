import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import json
import yaml
import csv

RULES_PATH = "rules"
OUTPUT_PATH = "output"

LOG_TYPES = {
    "Suricata": "suricata",
    "DNS": "dns"
}


def recursive_search(data, target_key):
    if isinstance(data, dict):
        for k, v in data.items():
            if k == target_key:
                yield v
            yield from recursive_search(v, target_key)
    elif isinstance(data, list):
        for item in data:
            yield from recursive_search(item, target_key)


def match_rules_txt(lines, rules):
    alerts = []
    summary = {}
    for idx, line in enumerate(lines):
        for rule in rules:
            if rule["match"].lower() in line.lower():
                alerts.append({
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "line": line.strip(),
                    "line_number": idx + 1
                })
                summary[rule["name"]] = summary.get(rule["name"], 0) + 1
    return alerts, summary


def match_rules_json(logs, rules):
    alerts = []
    summary = {}
    for idx, entry in enumerate(logs):
        layers = entry.get("_source", {}).get("layers", {})
        for rule in rules:
            key = rule.get("match_key")
            value = rule.get("match_value")
            found_values = list(recursive_search(layers, key))
            if any(str(value).lower() in str(v).lower() for v in found_values):
                alerts.append({
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "line": f'"{key}": "{value}"',
                    "line_number": idx + 1
                })
                summary[rule["name"]] = summary.get(rule["name"], 0) + 1
    return alerts, summary


def load_rules(log_type):
    rule_file = os.path.join(RULES_PATH, log_type, "rules.yaml")
    if not os.path.exists(rule_file):
        messagebox.showerror("Missing Rules", f"No rules found at {rule_file}")
        return []
    with open(rule_file, "r") as f:
        return yaml.safe_load(f)


def save_results(alerts, summary):
    os.makedirs(OUTPUT_PATH, exist_ok=True)

    with open(os.path.join(OUTPUT_PATH, "alerts.json"), "w") as jf:
        json.dump(alerts, jf, indent=4)

    with open(os.path.join(OUTPUT_PATH, "alerts.csv"), "w", newline='') as cf:
        writer = csv.writer(cf)
        writer.writerow(["Rule Name", "Severity", "Match Count"])
        for rule, count in summary.items():
            severity = next((a["severity"] for a in alerts if a["rule_name"] == rule), "unknown")
            writer.writerow([rule, severity, count])


# ================= GUI =================

class SIEMGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple SIEM Log Analyzer")
        self.root.geometry("700x500")

        self.log_type_var = tk.StringVar()
        self.log_file_path = tk.StringVar()

        ttk.Label(root, text="Log Type:").pack(pady=10)
        self.dropdown = ttk.Combobox(root, textvariable=self.log_type_var, values=list(LOG_TYPES.keys()), state="readonly")
        self.dropdown.pack()

        ttk.Button(root, text="Select Log File", command=self.browse_file).pack(pady=10)
        self.path_label = ttk.Label(root, textvariable=self.log_file_path)
        self.path_label.pack()

        ttk.Button(root, text="Analyze", command=self.analyze).pack(pady=15)

        self.alert_output = tk.Text(root, height=10, wrap="word")
        self.alert_output.pack(fill="both", expand=True, padx=10, pady=10)

    def browse_file(self):
        filetypes = [("Log files", "*.txt *.json"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Choose Log File", filetypes=filetypes)
        if file_path:
            self.log_file_path.set(file_path)

    def analyze(self):
        log_type_key = self.log_type_var.get()
        if not log_type_key or not self.log_file_path.get():
            messagebox.showwarning("Input Required", "Please select log type and file.")
            return

        file_path = self.log_file_path.get()
        log_type = LOG_TYPES[log_type_key]
        rules = load_rules(log_type)
        if not rules:
            return

        try:
            if file_path.endswith(".json"):
                with open(file_path, "r") as f:
                    logs = json.load(f)
                alerts, summary = match_rules_json(logs, rules)
                total_lines = len(logs)
            else:
                with open(file_path, "r") as f:
                    lines = f.readlines()
                alerts, summary = match_rules_txt(lines, rules)
                total_lines = len(lines)

            self.alert_output.delete("1.0", tk.END)

            self.alert_output.insert(tk.END, "=== Alerts ===\n")
            for alert in alerts:
                self.alert_output.insert(tk.END,
                    f"[{alert['severity'].upper()}] Line {alert['line_number']}: {alert['rule_name']} → {alert['line']}\n")

            self.alert_output.insert(tk.END, "\n=== Summary ===\n")
            self.alert_output.insert(tk.END, f"Lines scanned: {total_lines}\n")
            self.alert_output.insert(tk.END, f"Alerts triggered: {len(alerts)}\n")
            for rule, count in summary.items():
                self.alert_output.insert(tk.END, f" - {rule}: {count} matches\n")

            save_results(alerts, summary)
            self.alert_output.insert(tk.END, "\n✔ Results saved to output/alerts.json and alerts.csv\n")

        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    root = tk.Tk()
    app = SIEMGUI(root)
    root.mainloop()
