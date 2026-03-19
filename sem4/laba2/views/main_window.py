"""Main window view."""
import tkinter as tk
from tkinter import ttk, messagebox, Menu
from typing import Optional
from config import APP_TITLE, APP_WIDTH, APP_HEIGHT, COLUMNS, DEFAULT_ROWS_PER_PAGE, ROWS_PER_PAGE_OPTIONS
from utils.constants import Messages


class MainWindow:
    """Main application window."""

    def __init__(self, controller):
        self.controller = controller
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry(f"{APP_WIDTH}x{APP_HEIGHT}")

        self.current_page_var = tk.StringVar(value="1")
        self.total_pages_var = tk.StringVar(value="1")
        self.total_records_var = tk.StringVar(value="0")
        self.rows_per_page_var = tk.IntVar(value=DEFAULT_ROWS_PER_PAGE)

        self._setup_ui()
        self._setup_menu()
        self._setup_toolbar()

    def _setup_ui(self):
        """Setup the main UI components."""
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        table_frame = ttk.Frame(main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        self.tree = ttk.Treeview(table_frame, columns=COLUMNS, show='headings', height=15)

        vsb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        for col in COLUMNS:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, minwidth=100)

        self.tree.grid(row=0, column=0, sticky='nsew')
        vsb.grid(row=0, column=1, sticky='ns')
        hsb.grid(row=1, column=0, sticky='ew')

        table_frame.grid_rowconfigure(0, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)

        self._setup_pagination(main_frame)

    def _setup_pagination(self, parent):
        """Setup pagination controls."""
        pagination_frame = ttk.Frame(parent)
        pagination_frame.pack(fill=tk.X, pady=(10, 0))

        left_frame = ttk.Frame(pagination_frame)
        left_frame.pack(side=tk.LEFT)

        ttk.Label(left_frame, text="Записей на странице:").pack(side=tk.LEFT)
        rows_per_page_combo = ttk.Combobox(left_frame, textvariable=self.rows_per_page_var,
                                          values=ROWS_PER_PAGE_OPTIONS, width=5, state='readonly')
        rows_per_page_combo.pack(side=tk.LEFT, padx=(5, 0))
        rows_per_page_combo.bind('<<ComboboxSelected>>',
                                lambda e: self.controller.change_rows_per_page())

        center_frame = ttk.Frame(pagination_frame)
        center_frame.pack(side=tk.LEFT, expand=True)

        ttk.Button(center_frame, text="<<", width=3,
                  command=self.controller.first_page).pack(side=tk.LEFT)
        ttk.Button(center_frame, text="<", width=3,
                  command=self.controller.previous_page).pack(side=tk.LEFT)

        ttk.Label(center_frame, text="Страница:").pack(side=tk.LEFT, padx=(10, 5))
        page_entry = ttk.Entry(center_frame, textvariable=self.current_page_var, width=5)
        page_entry.pack(side=tk.LEFT)
        page_entry.bind('<Return>', lambda e: self.controller.go_to_page())

        ttk.Label(center_frame, text="из").pack(side=tk.LEFT, padx=5)
        ttk.Label(center_frame, textvariable=self.total_pages_var).pack(side=tk.LEFT)

        ttk.Button(center_frame, text=">", width=3,
                  command=self.controller.next_page).pack(side=tk.LEFT, padx=(10, 0))
        ttk.Button(center_frame, text=">>", width=3,
                  command=self.controller.last_page).pack(side=tk.LEFT)

        right_frame = ttk.Frame(pagination_frame)
        right_frame.pack(side=tk.RIGHT)

        ttk.Label(right_frame, text="Всего записей:").pack(side=tk.LEFT)
        ttk.Label(right_frame, textvariable=self.total_records_var).pack(side=tk.LEFT, padx=(5, 0))

    def _setup_menu(self):
        """Setup the main menu."""
        menubar = Menu(self.root)
        self.root.config(menu=menubar)

        file_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Файл", menu=file_menu)
        file_menu.add_command(label="Сохранить", command=self.controller.save_to_file,
                             accelerator="Ctrl+S")
        file_menu.add_command(label="Загрузить", command=self.controller.load_from_file,
                             accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Выход", command=self.controller.exit_app,
                             accelerator="Ctrl+Q")

        edit_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Правка", menu=edit_menu)
        edit_menu.add_command(label="Добавить", command=self.controller.show_add_dialog,
                             accelerator="Ctrl+N")
        edit_menu.add_command(label="Поиск", command=self.controller.show_search_dialog,
                             accelerator="Ctrl+F")
        edit_menu.add_command(label="Удалить", command=self.controller.show_delete_dialog,
                             accelerator="Ctrl+D")

        help_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Справка", menu=help_menu)
        help_menu.add_command(label="О программе", command=self.controller.show_about)

        self.root.bind('<Control-s>', lambda e: self.controller.save_to_file())
        self.root.bind('<Control-o>', lambda e: self.controller.load_from_file())
        self.root.bind('<Control-n>', lambda e: self.controller.show_add_dialog())
        self.root.bind('<Control-f>', lambda e: self.controller.show_search_dialog())
        self.root.bind('<Control-d>', lambda e: self.controller.show_delete_dialog())
        self.root.bind('<Control-q>', lambda e: self.controller.exit_app())

    def _setup_toolbar(self):
        """Setup the toolbar."""
        toolbar = ttk.Frame(self.root)
        toolbar.pack(fill=tk.X, padx=5, pady=5)

        ttk.Button(toolbar, text="Сохранить",
                  command=self.controller.save_to_file).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Загрузить",
                  command=self.controller.load_from_file).pack(side=tk.LEFT, padx=2)
        ttk.Separator(toolbar, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=5)
        ttk.Button(toolbar, text="Добавить",
                  command=self.controller.show_add_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Поиск",
                  command=self.controller.show_search_dialog).pack(side=tk.LEFT, padx=2)
        ttk.Button(toolbar, text="Удалить",
                  command=self.controller.show_delete_dialog).pack(side=tk.LEFT, padx=2)

    def update_table(self, products):
        """Update the table with products."""
        for item in self.tree.get_children():
            self.tree.delete(item)

        for product in products:
            quantity_display = str(product.stock_quantity) if product.stock_quantity > 0 else "нет на складе"
            self.tree.insert('', tk.END, values=(
                product.product_name,
                product.manufacturer_name,
                product.manufacturer_unp,
                quantity_display,
                product.warehouse_address
            ))

    def update_pagination_info(self, current_page, total_pages, total_records):
        """Update pagination information display."""
        self.current_page_var.set(str(current_page))
        self.total_pages_var.set(str(total_pages))
        self.total_records_var.set(str(total_records))

    def show_message(self, title, message, is_error=False):
        """Show a message dialog."""
        if is_error:
            messagebox.showerror(title, message)
        else:
            messagebox.showinfo(title, message)

    def ask_yes_no(self, title, message):
        """Ask a yes/no question."""
        return messagebox.askyesno(title, message)

    def run(self):
        """Start the main loop."""
        self.root.mainloop()

    def quit(self):
        """Quit the application."""
        self.root.quit()