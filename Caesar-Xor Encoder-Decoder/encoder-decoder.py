import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QTabWidget, QComboBox, QTextEdit
)

def caesar_cipher(text, shift, mode='encode'):
    result = ''
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            shift_val = shift if mode == 'encode' else -shift
            result += chr((ord(char) - base + shift_val) % 26 + base)
        else:
            result += char
    return result

def xor_cipher(text, key):
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(text))

class CipherTab(QWidget):
    def __init__(self, mode):
        super().__init__()
        self.mode = mode  # 'encode' or 'decode'
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.cipher_select = QComboBox()
        self.cipher_select.addItems(['Caesar', 'XOR'])
        layout.addWidget(QLabel("🔢 Cipher Type:"))
        layout.addWidget(self.cipher_select)

        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter your text here")
        layout.addWidget(QLabel("📝 Input Text:"))
        layout.addWidget(self.input_text)

        self.param_input = QLineEdit()
        self.param_input.setPlaceholderText("Shift (Caesar) or Key (XOR)")
        layout.addWidget(QLabel("🔐 Key or Shift:"))
        layout.addWidget(self.param_input)

        self.result_box = QTextEdit()
        self.result_box.setReadOnly(True)
        layout.addWidget(QLabel("📤 Result:"))
        layout.addWidget(self.result_box)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_cipher)
        layout.addWidget(self.run_button)

        self.setLayout(layout)

    def run_cipher(self):
        text = self.input_text.toPlainText()
        param = self.param_input.text()
        cipher_type = self.cipher_select.currentText()

        if cipher_type == 'Caesar':
            try:
                shift = int(param)
                result = caesar_cipher(text, shift, mode=self.mode)
            except ValueError:
                result = "❌ Invalid shift value. Must be an integer."
        elif cipher_type == 'XOR':
            if not param:
                result = "❌ Please enter a key for XOR."
            else:
                result = xor_cipher(text, param)
                if self.mode == 'decode':
                    try:
                        result = xor_cipher(text, param)
                    except:
                        result = "❌ Decoding failed."
        else:
            result = "❌ Invalid cipher selected."

        self.result_box.setText(result)

class CipherApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Caesar/XOR Encoder-Decoder")
        self.resize(600, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        tabs = QTabWidget()
        self.encode_tab = CipherTab(mode='encode')
        self.decode_tab = CipherTab(mode='decode')

        tabs.addTab(self.encode_tab, "🔐 Encode")
        tabs.addTab(self.decode_tab, "🔓 Decode")

        layout.addWidget(tabs)
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CipherApp()
    window.show()
    sys.exit(app.exec_())
