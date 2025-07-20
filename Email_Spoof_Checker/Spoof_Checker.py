import sys
import dns.resolver
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit
)

def count_spf_dns_lookups(spf_record):
    return sum(spf_record.count(x) for x in ["include:", "a", "mx", "ptr", "exists"])

def check_dkim(domain):
    selectors = ["default", "selector1", "google", "mail", "smtp", "20221208"]
    for selector in selectors:
        try:
            query = f"{selector}._domainkey.{domain}"
            answers = dns.resolver.resolve(query, 'TXT')
            for rdata in answers:
                if "v=DKIM1" in rdata.to_text():
                    return f"✅ DKIM record found with selector: {selector}"
        except:
            continue
    return "❌ No DKIM record found (common selectors tried)"

def generate_verdict(score):
    if score >= 5:
        return "✅ Verdict: Secure Email Configuration"
    elif score >= 3:
        return "⚠️ Verdict: Acceptable but improvable"
    else:
        return "❌ Verdict: Poor email protection – spoofing risk"

class EmailSecurityChecker(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("📤 Email Spoof Check Tool")
        self.setGeometry(300, 300, 650, 450)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.domain_input = QLineEdit()
        self.domain_input.setPlaceholderText("Enter domain (e.g., example.com)")
        input_layout.addWidget(self.domain_input)

        self.check_button = QPushButton("Check Email Security")
        self.check_button.clicked.connect(self.run_scan)
        input_layout.addWidget(self.check_button)

        layout.addLayout(input_layout)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def run_scan(self):
        domain = self.domain_input.text().strip()
        if not domain:
            self.result_box.setText("⚠️ Please enter a valid domain.")
            return

        self.result_box.setText(f"🔍 Scanning: {domain}\n")
        output = []
        score = 0
        recommendations = []

        spf = self.check_spf(domain)
        if "v=spf1" in spf:
            output.append(f"✅ SPF Record:\n   {spf}")
            warnings, spf_score = self.analyze_spf(spf)
            for w in warnings:
                output.append(f"   {w}")
            dns_count = count_spf_dns_lookups(spf)
            output.append(f"🔎 Resolved SPF Records: {dns_count}")
            if dns_count > 10:
                output.append("🚨 Too many DNS lookups – may exceed SPF limits")
                recommendations.append("➡️ Simplify SPF includes to stay under 10 DNS lookups.")
                score -= 1
            score += spf_score
            if "~all" in spf:
                recommendations.append("➡️ Consider using '-all' in SPF for stricter enforcement.")
        else:
            output.append(spf)
            score -= 2
            recommendations.append("➡️ Add an SPF record for sender validation.")

        output.append("")

        dmarc = self.check_dmarc(domain)
        if "v=DMARC1" in dmarc:
            output.append(f"✅ DMARC Record:\n   {dmarc}")
            warnings, dmarc_score, policy = self.analyze_dmarc(dmarc)
            for w in warnings:
                output.append(w)
            if "p=none" in dmarc:
                recommendations.append("➡️ Update DMARC policy to 'quarantine' or 'reject'.")
            if "sp=" in dmarc:
                output.append("📦 Subdomain Policy detected")
            score += dmarc_score
        else:
            output.append(dmarc)
            score -= 2
            recommendations.append("➡️ Add a DMARC record to protect from spoofing.")

        output.append("")

        dkim_result = check_dkim(domain)
        output.append(f"🔏 DKIM Check:\n   {dkim_result}")
        if dkim_result.startswith("✅"):
            score += 1
        else:
            score -= 1
            recommendations.append("➡️ Add a DKIM record with a strong selector.")

        output.append("")
        output.append(f"🛡️ Email Security Score: {score}/6")
        output.append(generate_verdict(score))

        if recommendations:
            output.append("\n🧠 Recommendations:")
            output.extend(recommendations)

        self.result_box.setText("\n".join(output))

    def check_spf(self, domain):
        try:
            answers = dns.resolver.resolve(domain, 'TXT')
            for rdata in answers:
                txt_record = rdata.to_text().strip('"')
                if txt_record.startswith("v=spf1"):
                    return txt_record
            return "❌ No SPF record found."
        except Exception as e:
            return f"❌ Error fetching SPF: {str(e)}"

    def check_dmarc(self, domain):
        try:
            dmarc_domain = f"_dmarc.{domain}"
            answers = dns.resolver.resolve(dmarc_domain, 'TXT')
            for rdata in answers:
                txt_record = rdata.to_text().strip('"')
                if txt_record.startswith("v=DMARC1"):
                    return txt_record
            return "❌ No DMARC record found."
        except Exception as e:
            return f"❌ Error fetching DMARC: {str(e)}"

    def analyze_spf(self, spf_record):
        score = 0
        warnings = []
        if "+all" in spf_record:
            warnings.append("🚨 SPF uses +all – allows all senders (very insecure)")
            score -= 3
        elif "~all" in spf_record:
            warnings.append("⚠️ SPF uses ~all – soft fail")
            score += 1
        elif "-all" in spf_record:
            warnings.append("✅ SPF uses -all – strict")
            score += 2
        else:
            warnings.append("⚠️ SPF missing 'all' mechanism")
        if spf_record.count("include:") > 5:
            warnings.append("⚠️ Too many include: statements – risk of DNS query limit")
            score -= 1
        return warnings, score

    def analyze_dmarc(self, dmarc_record):
        score = 0
        warnings = []
        if "p=reject" in dmarc_record:
            warnings.append("✅ Policy: reject – strict enforcement")
            score += 2
        elif "p=quarantine" in dmarc_record:
            warnings.append("⚠️ Policy: quarantine – moderate enforcement")
            score += 1
        elif "p=none" in dmarc_record:
            warnings.append("⚠️ Policy: none – weak enforcement")
            score -= 1
        else:
            warnings.append("❌ No clear DMARC policy found")
            score -= 2
        return warnings, score, dmarc_record

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = EmailSecurityChecker()
    window.show()
    sys.exit(app.exec_())
