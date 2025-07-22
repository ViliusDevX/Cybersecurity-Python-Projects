import sys
import socket
import threading
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QTextEdit
)

class PortScanner(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🌐 Simple Port Scanner")
        self.setGeometry(300, 300, 700, 500)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        input_layout = QHBoxLayout()
        self.target_input = QLineEdit()
        self.target_input.setPlaceholderText("Enter target IP or domain (e.g., scanme.nmap.org)")
        input_layout.addWidget(self.target_input)

        self.start_port_input = QLineEdit()
        self.start_port_input.setPlaceholderText("Start port")
        self.start_port_input.setFixedWidth(100)
        input_layout.addWidget(self.start_port_input)

        self.end_port_input = QLineEdit()
        self.end_port_input.setPlaceholderText("End port")
        self.end_port_input.setFixedWidth(100)
        input_layout.addWidget(self.end_port_input)

        self.scan_button = QPushButton("Start Scan")
        self.scan_button.clicked.connect(self.start_scan)
        input_layout.addWidget(self.scan_button)

        layout.addLayout(input_layout)

        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        layout.addWidget(self.output_box)

        self.setLayout(layout)

    def start_scan(self):
        self.output_box.clear()
        target = self.target_input.text().strip()
        try:
            start_port = int(self.start_port_input.text())
            end_port = int(self.end_port_input.text())
        except ValueError:
            self.output_box.setText("⚠️ Invalid port range.")
            return

        if not target or start_port < 1 or end_port > 65535 or start_port > end_port:
            self.output_box.setText("⚠️ Please check your input values.")
            return

        self.output_box.append(f"🔍 Scanning {target} from port {start_port} to {end_port}...\n")
        threading.Thread(target=self.scan_ports, args=(target, start_port, end_port), daemon=True).start()

    def scan_ports(self, target, start_port, end_port):
        for port in range(start_port, end_port + 1):
            threading.Thread(target=self.scan_port, args=(target, port), daemon=True).start()

    def scan_port(self, target, port):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            result = sock.connect_ex((target, port))
            if result == 0:
                banner = self.get_banner(sock)
                self.output_box.append(f"✅ Port {port} is open ({banner})")
            sock.close()
        except Exception as e:
            pass

    def get_banner(self, sock):
        try:
            sock.settimeout(1.0)
            banner = sock.recv(1024)
            try:
                return banner.decode('utf-8').strip()
            except UnicodeDecodeError:
                return "⚠️ Open (non-readable banner)"
        except:
            return "⚠️ Open (no response)"

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PortScanner()
    window.show()
    sys.exit(app.exec_())
