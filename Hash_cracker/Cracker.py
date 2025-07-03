import sys
import hashlib
import time
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit,
    QPushButton, QVBoxLayout, QFileDialog, QTextEdit
)

def detect_hash_type(hash_str):
    hash_length_map = {
        32: ['md5'],
        40: ['sha1', 'ripemd160'],
        56: ['sha224'],
        64: ['sha256', 'sha3_256', 'blake2s'],
        96: ['sha384', 'sha3_384'],
        128: ['sha512', 'sha3_512', 'blake2b']
    }
    return hash_length_map.get(len(hash_str), [])

def crack_hash(target_hash, hash_type, wordlist_path):
    try:
        with open(wordlist_path, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                password = line.strip()
                if not password:
                    continue
                h = hashlib.new(hash_type)
                h.update(password.encode("utf-8"))
                if h.hexdigest() == target_hash:
                    return password
    except Exception as e:
        return f"Error: {str(e)}"
    return None

class HashCrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hash Cracker (PyQt5)")
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.hash_input = QLineEdit()
        self.hash_input.setPlaceholderText("Enter hash to crack")
        layout.addWidget(QLabel("🔐 Hash:"))
        layout.addWidget(self.hash_input)

        self.hash_type_input = QLineEdit()
        self.hash_type_input.setPlaceholderText("Leave empty to auto-detect")
        layout.addWidget(QLabel("🔍 Hash type (optional):"))
        layout.addWidget(self.hash_type_input)

        self.wordlist_path = QLineEdit()
        self.wordlist_path.setPlaceholderText("Wordlist path (e.g., rockyou.txt)")
        layout.addWidget(QLabel("📂 Wordlist Path:"))
        layout.addWidget(self.wordlist_path)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)
        layout.addWidget(browse_button)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(self.result_box)

        crack_button = QPushButton("🔥 Crack Hash")
        crack_button.clicked.connect(self.run_cracker)
        layout.addWidget(crack_button)

        self.setLayout(layout)

    def browse_file(self):
        path, _ = QFileDialog.getOpenFileName(self, "Select Wordlist File")
        if path:
            self.wordlist_path.setText(path)

    def run_cracker(self):
        target_hash = self.hash_input.text().strip().lower()
        hash_type = self.hash_type_input.text().strip().lower()
        wordlist = self.wordlist_path.text().strip()

        if not target_hash:
            self.result_box.setText("⚠️ Please enter a hash to crack.")
            return

        if not wordlist:
            wordlist = "rockyou.txt"

        if not hash_type:
            possible = detect_hash_type(target_hash)
            if not possible:
                self.result_box.setText("❌ Could not auto-detect hash type.")
                return
            hash_type = possible[0]

        self.result_box.setText("🧠 Cracking started...\n")
        start = time.time()
        result = crack_hash(target_hash, hash_type, wordlist)
        end = time.time()

        if result is None:
            self.result_box.append("❌ Password not found in the wordlist.")
        elif result.startswith("Error:"):
            self.result_box.append(result)
        else:
            self.result_box.append(f"✅ Password found: {result}")

        self.result_box.append(f"⏱️ Time: {end - start:.2f} seconds")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HashCrackerApp()
    window.resize(500, 400)
    window.show()
    sys.exit(app.exec_())
