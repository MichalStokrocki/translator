import tkinter as tk
from tkinter import filedialog, messagebox
import argostranslate.package
import argostranslate.translate
import os


class Translator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)

