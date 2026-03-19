"""Delete dialog with specific criteria."""
import tkinter as tk
from tkinter import ttk, messagebox


class DeleteDialog:
    """Dialog for deleting products by specific criteria."""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Удаление товаров")
        self.dialog.geometry("600x650")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.product_name_var = tk.StringVar()
        self.stock_quantity_var = tk.StringVar()
        self.use_product_name = tk.BooleanVar(value=False)
        self.use_stock_quantity = tk.BooleanVar(value=False)

        self.manufacturer_name_var = tk.StringVar()
        self.manufacturer_unp_var = tk.StringVar()
        self.use_manufacturer_name = tk.BooleanVar(value=False)
        self.use_manufacturer_unp = tk.BooleanVar(value=False)

        self.warehouse_address_var = tk.StringVar()
        self.use_warehouse_address = tk.BooleanVar(value=False)

        self._setup_ui()
        self._center_dialog()

    def _setup_ui(self):
        """Setup the dialog UI."""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text="Условия удаления", font=('Arial', 14, 'bold'))
        title_label.pack(pady=(0, 20))

        warning_frame = ttk.LabelFrame(main_frame, text="⚠ Внимание", padding="10")
        warning_frame.pack(fill=tk.X, pady=(0, 20))

        warning_text = "Удаление производится по комбинации условий:\n" \
                       "• Внутри группы используется логическое ИЛИ\n" \
                       "• Между группами используется логическое И\n" \
                       "• Удаление нельзя отменить!"

        warning_label = ttk.Label(warning_frame, text=warning_text, justify=tk.LEFT)
        warning_label.pack()

        group1 = ttk.LabelFrame(main_frame, text="Критерии по товару", padding="10")
        group1.pack(fill=tk.X, pady=(0, 15))

        cb1_frame = ttk.Frame(group1)
        cb1_frame.pack(fill=tk.X, pady=2)

        self.cb1 = ttk.Checkbutton(cb1_frame, text="Название товара:",
                                   variable=self.use_product_name)
        self.cb1.pack(side=tk.LEFT)

        self.product_entry = ttk.Entry(cb1_frame, textvariable=self.product_name_var, width=40)
        self.product_entry.pack(side=tk.LEFT, padx=(10, 0))

        cb2_frame = ttk.Frame(group1)
        cb2_frame.pack(fill=tk.X, pady=2)

        self.cb2 = ttk.Checkbutton(cb2_frame, text="Количество на складе:",
                                   variable=self.use_stock_quantity)
        self.cb2.pack(side=tk.LEFT)

        quantity_frame = ttk.Frame(cb2_frame)
        quantity_frame.pack(side=tk.LEFT, padx=(10, 0))

        self.quantity_entry = ttk.Entry(quantity_frame, textvariable=self.stock_quantity_var, width=10)
        self.quantity_entry.pack(side=tk.LEFT)

        ttk.Label(quantity_frame, text="(0 - нет на складе)").pack(side=tk.LEFT, padx=(5, 0))

        group2 = ttk.LabelFrame(main_frame, text="Критерии по производителю", padding="10")
        group2.pack(fill=tk.X, pady=(0, 15))

        cb3_frame = ttk.Frame(group2)
        cb3_frame.pack(fill=tk.X, pady=2)

        self.cb3 = ttk.Checkbutton(cb3_frame, text="Название производителя:",
                                   variable=self.use_manufacturer_name)
        self.cb3.pack(side=tk.LEFT)

        self.manufacturer_entry = ttk.Entry(cb3_frame, textvariable=self.manufacturer_name_var, width=40)
        self.manufacturer_entry.pack(side=tk.LEFT, padx=(10, 0))

        cb4_frame = ttk.Frame(group2)
        cb4_frame.pack(fill=tk.X, pady=2)

        self.cb4 = ttk.Checkbutton(cb4_frame, text="УНП производителя:",
                                   variable=self.use_manufacturer_unp)
        self.cb4.pack(side=tk.LEFT)

        self.unp_entry = ttk.Entry(cb4_frame, textvariable=self.manufacturer_unp_var, width=20)
        self.unp_entry.pack(side=tk.LEFT, padx=(10, 0))

        group3 = ttk.LabelFrame(main_frame, text="Критерии по адресу", padding="10")
        group3.pack(fill=tk.X, pady=(0, 15))

        cb5_frame = ttk.Frame(group3)
        cb5_frame.pack(fill=tk.X, pady=2)

        self.cb5 = ttk.Checkbutton(cb5_frame, text="Адрес склада:",
                                   variable=self.use_warehouse_address)
        self.cb5.pack(side=tk.LEFT)

        self.address_entry = ttk.Entry(cb5_frame, textvariable=self.warehouse_address_var, width=40)
        self.address_entry.pack(side=tk.LEFT, padx=(10, 0))

        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=(30, 10))

        self.delete_button = ttk.Button(button_frame, text="Удалить",
                                        command=self._delete,
                                        width=15)
        self.delete_button.pack(side=tk.LEFT, padx=5)

        self.cancel_button = ttk.Button(button_frame, text="Отмена",
                                        command=self.dialog.destroy,
                                        width=15)
        self.cancel_button.pack(side=tk.LEFT, padx=5)

        extra_warning = ttk.Label(main_frame,
                                  text="⚠ Удаление нельзя отменить!",
                                  foreground="red",
                                  font=('Arial', 10, 'bold'))
        extra_warning.pack(pady=(5, 0))

    def _center_dialog(self):
        """Center the dialog on the parent window."""
        self.dialog.update_idletasks()

        parent_x = self.parent.winfo_rootx()
        parent_y = self.parent.winfo_rooty()
        parent_width = self.parent.winfo_width()
        parent_height = self.parent.winfo_height()

        dialog_width = self.dialog.winfo_width()
        dialog_height = self.dialog.winfo_height()

        x = parent_x + (parent_width - dialog_width) // 2
        y = parent_y + (parent_height - dialog_height) // 2

        self.dialog.geometry(f"+{x}+{y}")

    def _delete(self):
        """Delete products based on selected criteria."""
        try:
            selected_criteria = []
            if self.use_product_name.get() and self.product_name_var.get().strip():
                selected_criteria.append("название товара")
            if self.use_stock_quantity.get() and self.stock_quantity_var.get().strip():
                selected_criteria.append("количество")
            if self.use_manufacturer_name.get() and self.manufacturer_name_var.get().strip():
                selected_criteria.append("название производителя")
            if self.use_manufacturer_unp.get() and self.manufacturer_unp_var.get().strip():
                selected_criteria.append("УНП")
            if self.use_warehouse_address.get() and self.warehouse_address_var.get().strip():
                selected_criteria.append("адрес склада")

            if not selected_criteria:
                messagebox.showwarning(
                    "Предупреждение",
                    "Выберите хотя бы один критерий для удаления и заполните его значение"
                )
                return

            all_products = self.controller.model.products.copy()
            products_to_delete = []

            for product in all_products:
                match_group1 = True
                match_group2 = True
                match_group3 = True

                if self.use_product_name.get() or self.use_stock_quantity.get():
                    match_group1 = False

                    if self.use_product_name.get() and self.product_name_var.get().strip():
                        search_text = self.product_name_var.get().strip().lower()
                        if search_text in product.product_name.lower():
                            match_group1 = True

                    if self.use_stock_quantity.get() and self.stock_quantity_var.get().strip():
                        quantity_text = self.stock_quantity_var.get().strip()
                        try:
                            quantity = int(quantity_text)
                            if product.stock_quantity == quantity:
                                match_group1 = True
                        except ValueError:
                            if quantity_text.lower() == 'нет на складе' and product.stock_quantity == 0:
                                match_group1 = True

                if self.use_manufacturer_name.get() or self.use_manufacturer_unp.get():
                    match_group2 = False

                    if self.use_manufacturer_name.get() and self.manufacturer_name_var.get().strip():
                        search_text = self.manufacturer_name_var.get().strip().lower()
                        if search_text in product.manufacturer_name.lower():
                            match_group2 = True

                    if self.use_manufacturer_unp.get() and self.manufacturer_unp_var.get().strip():
                        if self.manufacturer_unp_var.get().strip() == product.manufacturer_unp:
                            match_group2 = True

                if self.use_warehouse_address.get() and self.warehouse_address_var.get().strip():
                    search_text = self.warehouse_address_var.get().strip().lower()
                    if search_text not in product.warehouse_address.lower():
                        match_group3 = False

                if match_group1 and match_group2 and match_group3:
                    products_to_delete.append(product)

            if not products_to_delete:
                messagebox.showinfo("Результат", "Записей для удаления не найдено")
                return

            criteria_text = ", ".join(selected_criteria)
            result = messagebox.askyesno(
                "Подтверждение удаления",
                f"Найдено записей для удаления: {len(products_to_delete)}\n"
                f"Критерии: {criteria_text}\n\n"
                "Вы уверены, что хотите удалить эти записи?\n"
                "Это действие нельзя отменить!",
                icon='warning'
            )

            if not result:
                return

            for product in products_to_delete:
                self.controller.model._products.remove(product)

            self.controller.model._notify_observers()

            messagebox.showinfo(
                "Успех",
                f"Удалено записей: {len(products_to_delete)}"
            )
            self.dialog.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при удалении: {str(e)}")