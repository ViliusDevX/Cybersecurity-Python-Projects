import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLineEdit, QPushButton,
    QVBoxLayout, QTextEdit, QHBoxLayout, QLabel
)

class IPInfoApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple IP Info Checker")
        self.setGeometry(100, 100, 500, 400)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        title = QLabel("🌐 Simple IP Info Checker")
        title.setStyleSheet("font-weight: bold; font-size: 18px;")
        layout.addWidget(title)

        input_layout = QHBoxLayout()
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address")
        input_layout.addWidget(self.ip_input)

        self.check_button = QPushButton("Check")
        self.check_button.clicked.connect(self.fetch_ip_info)
        input_layout.addWidget(self.check_button)

        layout.addLayout(input_layout)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def fetch_ip_info(self):
        ip = self.ip_input.text().strip()
        if not ip:
            self.result_box.setText("⚠️ Please enter a valid IP address.")
            return

        self.result_box.setText("🔍 Fetching IP information...\n")

        data = self.query_ip_api(ip)
        if not data:
            data = self.query_ipwhois(ip)

        if not data:
            self.result_box.append("❌ Failed to fetch data from both sources.")
            return

        output = self.format_ip_info(data)
        self.result_box.setText(output)

    def query_ip_api(self, ip):
        try:
            res = requests.get(f"http://ip-api.com/json/{ip}?fields=66846719", timeout=5)
            if res.status_code == 200:
                return res.json()
        except:
            return None

    def query_ipwhois(self, ip):
        try:
            res = requests.get(f"https://ipwho.is/{ip}", timeout=5)
            if res.status_code == 200:
                return res.json()
        except:
            return None

    def format_ip_info(self, data):
        output = []
        output.append(f"🌐 IP Address: {data.get('query') or data.get('ip')}")
        output.append(f"📍 Location: {data.get('city')}, {data.get('regionName') or data.get('region')}, {data.get('country')}")
        output.append(f"🏢 ISP: {data.get('isp') or data.get('connection', {}).get('isp')}")
        output.append(f"🔢 ASN: {data.get('as') or data.get('connection', {}).get('asn')}")
        output.append(f"🌍 Coordinates: {data.get('lat')}, {data.get('lon')}")
        output.append(f"🕒 Timezone: {data.get('timezone')}")
        output.append(f"🔒 Proxy/VPN: {data.get('privacy', {}).get('proxy', 'Unknown')}")
        return "\n".join(output)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = IPInfoApp()
    window.show()
    sys.exit(app.exec_())
