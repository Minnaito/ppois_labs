"""Add product dialog."""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from models.product import Product
from utils.constants import ValidationMessages


class AddProductDialog:
    """Dialog for adding a new product."""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Добавление товара")
        self.dialog.geometry("500x450")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.result = None
        self._setup_ui()
        self._center_dialog()

    def _setup_ui(self):
        """Setup the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Product name
        ttk.Label(main_frame, text="Название товара:*").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.product_name_entry = ttk.Entry(main_frame, width=50)
        self.product_name_entry.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Manufacturer name
        ttk.Label(main_frame, text="Название производителя:*").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.manufacturer_name_entry = ttk.Entry(main_frame, width=50)
        self.manufacturer_name_entry.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Manufacturer UNP
        ttk.Label(main_frame, text="УНП производителя:*").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.manufacturer_unp_entry = ttk.Entry(main_frame, width=20)
        self.manufacturer_unp_entry.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Stock quantity
        ttk.Label(main_frame, text="Количество на складе:*").grid(row=3, column=0, sticky=tk.W, pady=5)
        quantity_frame = ttk.Frame(main_frame)
        quantity_frame.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        self.stock_quantity_entry = ttk.Entry(quantity_frame, width=10)
        self.stock_quantity_entry.pack(side=tk.LEFT)

        ttk.Label(quantity_frame, text="(0 - нет на складе)").pack(side=tk.LEFT, padx=(5, 0))

        # Warehouse address
        ttk.Label(main_frame, text="Адрес склада:*").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.warehouse_address_entry = ttk.Entry(main_frame, width=50)
        self.warehouse_address_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Creation date (auto-generated)
        ttk.Label(main_frame, text="Дата создания:").grid(row=5, column=0, sticky=tk.W, pady=5)
        date_label = ttk.Label(main_frame, text=datetime.now().strftime("%d.%m.%Y %H:%M"))
        date_label.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        # Required fields note
        ttk.Label(main_frame, text="* - обязательные поля", foreground="gray").grid(
            row=6, column=0, columnspan=2, sticky=tk.W, pady=(20, 10))

        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0))

        ttk.Button(button_frame, text="Сохранить", command=self._save,
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Отмена", command=self.dialog.destroy,
                  width=15).pack(side=tk.LEFT, padx=5)

    def _center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()
        parent_x = self.parent.winfo_x()
        parent_y = self.parent.winfo_y()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"+{x}+{y}")

    def _save(self):
        """Save the product."""
        try:
            # Get values
            product_name = self.product_name_entry.get().strip()
            manufacturer_name = self.manufacturer_name_entry.get().strip()
            manufacturer_unp = self.manufacturer_unp_entry.get().strip()
            quantity_text = self.stock_quantity_entry.get().strip()
            warehouse_address = self.warehouse_address_entry.get().strip()

            # Validate
            if not product_name:
                raise ValueError(ValidationMessages.PRODUCT_NAME_REQUIRED.value)

            if not manufacturer_name:
                raise ValueError(ValidationMessages.MANUFACTURER_NAME_REQUIRED.value)

            if not manufacturer_unp:
                raise ValueError(ValidationMessages.MANUFACTURER_UNP_REQUIRED.value)

            if not manufacturer_unp.isdigit() or len(manufacturer_unp) != 9:
                raise ValueError(ValidationMessages.MANUFACTURER_UNP_INVALID.value)

            try:
                stock_quantity = int(quantity_text) if quantity_text else 0
                if stock_quantity < 0:
                    raise ValueError()
            except ValueError:
                raise ValueError(ValidationMessages.STOCK_QUANTITY_INVALID.value)

            if not warehouse_address:
                raise ValueError(ValidationMessages.WAREHOUSE_ADDRESS_REQUIRED.value)

            # Create product
            product = Product(
                product_name=product_name,
                manufacturer_name=manufacturer_name,
                manufacturer_unp=manufacturer_unp,
                stock_quantity=stock_quantity,
                warehouse_address=warehouse_address
            )

            self.result = product
            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Ошибка валидации", str(e))
