import tkinter as tk
from tkinter import filedialog, messagebox
import argostranslate.package
import argostranslate.translate
import os


class Translator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Translator")
        self.input_file_path = None

        self.choose_file_button = tk.Button(self.root, text="Wybierz Plik", command=self.choose_file)
        self.choose_file_button.grid(row=0, column=0, padx=10, pady=10)

        self.text_display = tk.Text(self.root, height=15, width=50, state=tk.DISABLED)
        self.text_display.grid(row=0, column=1, padx=10, pady=10)

        self.choose_save_button = tk.Button(self.root, text="Wybierz miejsce zapisu", command=self.choose_save_location)
        self.choose_save_button.grid(row=2, column=0, padx=10, pady=10)

        self.save_path_entry = tk.Entry(self.root, width=50)
        self.save_path_entry.grid(row=2, column=1, padx=10, pady=10)

        self.file_name_label = tk.Label(self.root, text="Nazwa pliku po przetłumaczeniu:")
        self.file_name_label.grid(row=3, column=0, padx=10, pady=10)

        self.file_name_entry = tk.Entry(self.root, width=50)
        self.file_name_entry.grid(row=3, column=1, padx=10, pady=10)

        self.translate_button = tk.Button(self.root, text="Tłumacz", command=self.translate_and_save)
        self.translate_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def choose_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            global input_file_path
            input_file_path = file_path
            self.make_preview()

    def make_preview(self):
        with open(input_file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            preview = ''.join(lines[:50])
            self.text_display.config(state=tk.NORMAL)
            self.text_display.delete(1.0, tk.END)
            self.text_display.insert(tk.END, preview)
            self.text_display.config(state=tk.DISABLED)

    def choose_save_location(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.save_path_entry.delete(0, tk.END)
            self.save_path_entry.insert(0, folder_path)


    def translate_and_save(self):
        from_code = "pl"
        to_code = "en"
        if not input_file_path:
            messagebox.showerror("Błąd", "Wybierz plik do przetłumaczenia.")
            return

        if not self.save_path_entry.get():
            messagebox.showerror("Błąd", "Wybierz miejsce zapisu pliku.")
            return

        if not self.file_name_entry.get():
            messagebox.showerror("Błąd", "Wybierz nazwe pliku.")
            return

        with open(input_file_path, 'r', encoding='utf-8') as file:
            text = file.read()

        translated_text = argostranslate.translate.translate(text, from_code, to_code)

        save_path = os.path.join(self.save_path_entry.get(), f"{self.file_name_entry.get()}.txt")
        with open(save_path, 'w', encoding='utf-8') as file:
            file.write(translated_text)

        messagebox.showinfo("Sukces", f"Plik przetłumaczony i zapisany w:{save_path}")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = Translator()
    app.run()