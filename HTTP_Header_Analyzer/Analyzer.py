import sys
import requests
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel,
    QLineEdit, QPushButton, QTextEdit, QMessageBox
)

class HeaderAnalyzer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("HTTP Header Analyzer")
        self.setGeometry(100, 100, 600, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Enter website URL (e.g., https://example.com)")
        layout.addWidget(QLabel("🔗 URL:"))
        layout.addWidget(self.url_input)

        self.analyze_button = QPushButton("Analyze Headers")
        self.analyze_button.clicked.connect(self.analyze_headers)
        layout.addWidget(self.analyze_button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(QLabel("📋 Results:"))
        layout.addWidget(self.result_box)

        self.setLayout(layout)

    def analyze_headers(self):
        url = self.url_input.text().strip()

        if not url.startswith("http"):
            url = "http://" + url

        try:
            response = requests.get(url, timeout=5)
            headers = response.headers
            self.display_results(response.status_code, headers)
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ Could not fetch headers:\n{str(e)}")

    def display_results(self, status_code, headers):
        output = []
        output.append(f"✅ Status Code: {status_code}")
        output.append("\n📌 Headers:\n")
        for key, value in headers.items():
            output.append(f"{key}: {value}")

        output.append("\n🔐 Security Header Check:")
        security_headers = [
            "Strict-Transport-Security",
            "Content-Security-Policy",
            "X-Content-Type-Options",
            "X-Frame-Options",
            "X-XSS-Protection",
            "Referrer-Policy",
            "Permissions-Policy"
        ]

        for header in security_headers:
            if header in headers:
                output.append(f"✔️ {header} is present")
            else:
                output.append(f"❌ {header} is missing")

        self.result_box.setText("\n".join(output))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HeaderAnalyzer()
    window.show()
    sys.exit(app.exec_())
