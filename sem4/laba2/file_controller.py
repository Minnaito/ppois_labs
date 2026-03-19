"""File operations controller."""
import os
from tkinter import filedialog, messagebox
from config import DEFAULT_FILE_EXTENSION, FILE_TYPE_FILTER
from parsers.xml_writer import XMLWriter
from parsers.xml_reader import XMLReader
from utils.constants import Messages


class FileController:
    """Handles file operations."""

    def __init__(self, parent_window):
        self.parent_window = parent_window

    def save_to_file(self, products):
        """Save products to XML file."""
        filename = filedialog.asksaveasfilename(
            parent=self.parent_window,
            title="Сохранить файл",
            defaultextension=DEFAULT_FILE_EXTENSION,
            filetypes=[(FILE_TYPE_FILTER, "*.xml"), ("All files", "*.*")]
        )

        if filename:
            try:
                XMLWriter.write_to_file(products, filename)
                messagebox.showinfo("Успех", Messages.SAVE_SUCCESS.value)
                return True
            except Exception as e:
                messagebox.showerror("Ошибка", Messages.SAVE_ERROR.value.format(str(e)))
                return False
        return False

    def load_from_file(self):
        """Load products from XML file."""
        filename = filedialog.askopenfilename(
            parent=self.parent_window,
            title="Загрузить файл",
            filetypes=[(FILE_TYPE_FILTER, "*.xml"), ("All files", "*.*")]
        )

        if filename:
            try:
                products = XMLReader.read_from_file(filename)
                messagebox.showinfo("Успех", Messages.LOAD_SUCCESS.value.format(len(products)))
                return products
            except Exception as e:
                messagebox.showerror("Ошибка", Messages.LOAD_ERROR.value.format(str(e)))
                return None
        return None