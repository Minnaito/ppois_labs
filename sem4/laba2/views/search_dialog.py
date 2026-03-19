"""Search dialog with specific criteria."""
import tkinter as tk
from tkinter import ttk, messagebox
from config import COLUMNS, ROWS_PER_PAGE_OPTIONS


class SearchDialog:
    """Dialog for searching products by specific criteria."""

    def __init__(self, parent, controller):
        self.parent = parent
        self.controller = controller
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Поиск товаров")
        self.dialog.geometry("900x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()

        self.search_results = []
        self.current_page = 1
        self.rows_per_page = tk.IntVar(value=10)
        self.total_pages = 1
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
        paned = ttk.PanedWindow(self.dialog, orient=tk.HORIZONTAL)
        paned.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        left_frame = ttk.Frame(paned, width=300)
        paned.add(left_frame, weight=1)

        self._setup_search_criteria(left_frame)

        right_frame = ttk.Frame(paned)
        paned.add(right_frame, weight=3)

        self._setup_results_area(right_frame)

    def _setup_search_criteria(self, parent):
        """Setup search criteria inputs with OR conditions."""
        # Title
        ttk.Label(parent, text="Критерии поиска", font=('Arial', 12, 'bold')).pack(pady=(0, 10))

        canvas = tk.Canvas(parent, highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        group1 = ttk.LabelFrame(scrollable_frame, text="Поиск по товару", padding="10")
        group1.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(group1, text="Название товара:",
                       variable=self.use_product_name).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(group1, textvariable=self.product_name_var, width=30).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Checkbutton(group1, text="Количество на складе:",
                       variable=self.use_stock_quantity).grid(row=1, column=0, sticky=tk.W, pady=5)
        quantity_frame = ttk.Frame(group1)
        quantity_frame.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Entry(quantity_frame, textvariable=self.stock_quantity_var, width=10).pack(side=tk.LEFT)
        ttk.Label(quantity_frame, text="(0 - нет на складе)").pack(side=tk.LEFT, padx=(5, 0))

        ttk.Label(group1, text="(будут найдены товары, соответствующие любому из выбранных критериев)",
                 foreground="gray", wraplength=250).grid(row=2, column=0, columnspan=2, pady=(5, 0))

        group2 = ttk.LabelFrame(scrollable_frame, text="Поиск по производителю", padding="10")
        group2.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(group2, text="Название производителя:",
                       variable=self.use_manufacturer_name).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(group2, textvariable=self.manufacturer_name_var, width=30).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Checkbutton(group2, text="УНП производителя:",
                       variable=self.use_manufacturer_unp).grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(group2, textvariable=self.manufacturer_unp_var, width=20).grid(
            row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(group2, text="(будут найдены товары, соответствующие любому из выбранных критериев)",
                 foreground="gray", wraplength=250).grid(row=2, column=0, columnspan=2, pady=(5, 0))

        group3 = ttk.LabelFrame(scrollable_frame, text="Поиск по адресу", padding="10")
        group3.pack(fill=tk.X, pady=(0, 10))

        ttk.Checkbutton(group3, text="Адрес склада:",
                       variable=self.use_warehouse_address).grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(group3, textvariable=self.warehouse_address_var, width=30).grid(
            row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))

        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(fill=tk.X, pady=(20, 10))

        ttk.Button(button_frame, text="Поиск", command=self._search,
                  width=15).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Очистить", command=self._clear_criteria,
                  width=15).pack(side=tk.LEFT, padx=5)

        info_frame = ttk.LabelFrame(scrollable_frame, text="Информация", padding="10")
        info_frame.pack(fill=tk.X, pady=(10, 0))

        info_text = """Правила поиска:
• Выберите нужные критерии с помощью флажков
• Внутри каждой группы используется логическое ИЛИ
• Между группами используется логическое И
• Пустые критерии игнорируются"""

        ttk.Label(info_frame, text=info_text, justify=tk.LEFT).pack(anchor=tk.W)

    def _setup_results_area(self, parent):
        """Setup results display area."""
        self.results_count_var = tk.StringVar(value="Найдено записей: 0")
        ttk.Label(parent, textvariable=self.results_count_var,
                 font=('Arial', 10, 'bold')).pack(anchor=tk.W, pady=(0, 10))

        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(tree_frame, columns=COLUMNS, show='headings', height=15)

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=100)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self._setup_pagination(parent)

    def _setup_pagination(self, parent):
        """Setup pagination controls."""
        pagination_frame = ttk.Frame(parent)
        pagination_frame.pack(fill=tk.X, pady=(10, 0))

        left_frame = ttk.Frame(pagination_frame)
        left_frame.pack(side=tk.LEFT)

        ttk.Label(left_frame, text="На странице:").pack(side=tk.LEFT)
        rows_combo = ttk.Combobox(left_frame, textvariable=self.rows_per_page,
                                  values=ROWS_PER_PAGE_OPTIONS, width=5, state='readonly')
        rows_combo.pack(side=tk.LEFT, padx=(5, 0))
        rows_combo.bind('<<ComboboxSelected>>', lambda e: self._change_rows_per_page())

        center_frame = ttk.Frame(pagination_frame)
        center_frame.pack(side=tk.LEFT, expand=True)

        self.page_buttons = {}
        self.page_buttons['first'] = ttk.Button(center_frame, text="<<", width=3,
                                                command=self._first_page)
        self.page_buttons['first'].pack(side=tk.LEFT)

        self.page_buttons['prev'] = ttk.Button(center_frame, text="<", width=3,
                                               command=self._previous_page)
        self.page_buttons['prev'].pack(side=tk.LEFT)

        self.page_label = ttk.Label(center_frame, text="Страница 1 из 1")
        self.page_label.pack(side=tk.LEFT, padx=10)

        self.page_buttons['next'] = ttk.Button(center_frame, text=">", width=3,
                                               command=self._next_page)
        self.page_buttons['next'].pack(side=tk.LEFT)

        self.page_buttons['last'] = ttk.Button(center_frame, text=">>", width=3,
                                               command=self._last_page)
        self.page_buttons['last'].pack(side=tk.LEFT)

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

    def _search(self):
        """Perform search based on selected criteria."""
        try:
            if not any([self.use_product_name.get(), self.use_stock_quantity.get(),
                       self.use_manufacturer_name.get(), self.use_manufacturer_unp.get(),
                       self.use_warehouse_address.get()]):
                messagebox.showwarning("Предупреждение", "Выберите хотя бы один критерий для поиска")
                return

            all_products = self.controller.model.products
            self.search_results = []

            for product in all_products:

                match_group1 = True
                match_group2 = True
                match_group3 = True

                if self.use_product_name.get() or self.use_stock_quantity.get():
                    match_group1 = False

                    if self.use_product_name.get() and self.product_name_var.get().strip():
                        if self.product_name_var.get().strip().lower() in product.product_name.lower():
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
                        if self.manufacturer_name_var.get().strip().lower() in product.manufacturer_name.lower():
                            match_group2 = True

                    if self.use_manufacturer_unp.get() and self.manufacturer_unp_var.get().strip():
                        if self.manufacturer_unp_var.get().strip() == product.manufacturer_unp:
                            match_group2 = True

                if self.use_warehouse_address.get() and self.warehouse_address_var.get().strip():
                    if self.warehouse_address_var.get().strip().lower() not in product.warehouse_address.lower():
                        match_group3 = False

                if match_group1 and match_group2 and match_group3:
                    self.search_results.append(product)

            self.total_pages = max(1, (len(self.search_results) + self.rows_per_page.get() - 1) // self.rows_per_page.get())
            self.current_page = 1
            self._update_results_display()
            self.results_count_var.set(f"Найдено записей: {len(self.search_results)}")

        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при поиске: {str(e)}")

    def _clear_criteria(self):
        """Clear all search criteria."""
        self.product_name_var.set("")
        self.stock_quantity_var.set("")
        self.manufacturer_name_var.set("")
        self.manufacturer_unp_var.set("")
        self.warehouse_address_var.set("")

        self.use_product_name.set(False)
        self.use_stock_quantity.set(False)
        self.use_manufacturer_name.set(False)
        self.use_manufacturer_unp.set(False)
        self.use_warehouse_address.set(False)

    def _update_results_display(self):
        """Update the results table with current page."""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)

        start = (self.current_page - 1) * self.rows_per_page.get()
        end = start + self.rows_per_page.get()
        page_data = self.search_results[start:end]

        for product in page_data:
            quantity_display = str(product.stock_quantity) if product.stock_quantity > 0 else "нет на складе"
            self.tree.insert('', tk.END, values=(
                product.product_name,
                product.manufacturer_name,
                product.manufacturer_unp,
                quantity_display,
                product.warehouse_address
            ))

        self.page_label.config(text=f"Страница {self.current_page} из {self.total_pages}")

        self.page_buttons['first'].config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.page_buttons['prev'].config(state=tk.NORMAL if self.current_page > 1 else tk.DISABLED)
        self.page_buttons['next'].config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)
        self.page_buttons['last'].config(state=tk.NORMAL if self.current_page < self.total_pages else tk.DISABLED)

    def _change_rows_per_page(self):
        """Change the number of rows per page."""
        if self.search_results:
            self.total_pages = max(1, (len(self.search_results) + self.rows_per_page.get() - 1) // self.rows_per_page.get())
            self.current_page = min(self.current_page, self.total_pages)
            self._update_results_display()

    def _first_page(self):
        """Go to first page."""
        self.current_page = 1
        self._update_results_display()

    def _previous_page(self):
        """Go to previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self._update_results_display()

    def _next_page(self):
        """Go to next page."""
        if self.current_page < self.total_pages:
            self.current_page += 1
            self._update_results_display()

    def _last_page(self):
        """Go to last page."""
        self.current_page = self.total_pages
        self._update_results_display()