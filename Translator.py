import sys

from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QTextEdit, QComboBox, QLineEdit, QFileDialog, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from tkinter import filedialog, messagebox
import argostranslate.package
import argostranslate.translate
import os


class Translator(QWidget):
    def __init__(self):
        super().__init__()
        self.translated_text = None
        self.file_name = None
        self.input_file_path = None
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Translator')
        self.layout = QVBoxLayout()

        self.choose_file_button = QPushButton('Wybierz Plik', self)
        self.choose_file_button.clicked.connect(self.choose_file)
        self.layout.addWidget(self.choose_file_button)

        self.text_display = QTextEdit(self)
        self.text_display.setReadOnly(True)
        self.layout.addWidget(self.text_display)

        self.choose_save_button = QPushButton('Wybierz miejsce zapisu', self)
        self.choose_save_button.clicked.connect(self.choose_save_location)
        self.layout.addWidget(self.choose_save_button)

        self.save_path_entry = QLineEdit(self)
        self.layout.addWidget(self.save_path_entry)

        self.file_name_label = QLabel('Nazwa nowego pliku:', self)
        self.layout.addWidget(self.file_name_label)

        self.file_name_entry = QLineEdit(self)
        self.layout.addWidget(self.file_name_entry)

        self.translate_button = QPushButton('Tłumacz', self)
        self.translate_button.clicked.connect(self.translate_and_save)
        self.layout.addWidget(self.translate_button)

        self.setLayout(self.layout)
        self.input_file_path = None

    def choose_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, 'Choose File', '', 'Text files (*.txt)', options=options)
        if file_path:
            temp = os.path.basename(file_path)
            name, ext = os.path.splitext(temp)
            if ext == ".txt":
                self.file_name = name + "-en"
            else:
                self.file_name = ext + "-en"
            with open(file_path, 'r', encoding='utf-8') as file:
                lines = file.readlines()
                preview = ''.join(lines[:50])
                self.text_display.setPlainText(preview)
            self.input_file_path = file_path

    def choose_save_location(self):
        options = QFileDialog.Options()
        folder_path = QFileDialog.getExistingDirectory(self, 'Wybierz miejsce zapisu', '', options=options)
        if folder_path:
            self.save_path_entry.setText(folder_path)
            self.file_name_entry.setText(self.file_name)

    def translate_and_save(self):
        from_code = "pl"
        to_code = "en"
        if not self.input_file_path:
            QMessageBox.critical(self, "Błąd", "Wybierz plik do przetłumaczenia.")
            return

        if not self.save_path_entry.text():
            QMessageBox.critical(self, "Błąd", "Wybierz miejsce zapisu pliku.")
            return

        if not self.file_name_entry.text():
            QMessageBox.critical(self, "Błąd", "Wybierz nazwe pliku.")
            return

        with open(self.input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        self.translated_text = argostranslate.translate.translate(text, from_code, to_code)

        save_path = os.path.join(self.save_path_entry.text(), f"{self.file_name_entry.text()}.txt")
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(self.translated_text)

        QMessageBox.information(self, "Sukces", f"Plik przetłumaczony i zapisany w {save_path}")

def main():
    app = QApplication(sys.argv)
    ex = Translator()
    ex.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
