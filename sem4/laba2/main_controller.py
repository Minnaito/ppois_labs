"""Main controller implementing MVC pattern."""
from tkinter import messagebox
from models.product_list import ProductList
from models.product import Product
from views.main_window import MainWindow
from views.add_product_dialog import AddProductDialog
from views.search_dialog import SearchDialog
from views.delete_dialog import DeleteDialog
from controllers.file_controller import FileController
from utils.constants import Messages


class MainController:
    """Main application controller."""

    def __init__(self):
        self.model = ProductList()
        self.view = None
        self.file_controller = None

        self.model.add_observer(self._on_model_changed)

    def run(self):
        """Start the application."""
        self.view = MainWindow(self)
        self.file_controller = FileController(self.view.root)

        self._update_view()

        self.view.run()

    def _on_model_changed(self):
        """Handle model changes."""
        self._update_view()

    def _update_view(self):
        """Update the view with current model data."""
        if self.view:
            products = self.model.get_page()

            self.view.update_table(products)

            self.view.update_pagination_info(
                self.model.current_page,
                self.model.total_pages,
                self.model.total_count
            )

    def add_product(self, product: Product) -> None:
        """Add a new product."""
        try:
            self.model.add_product(product)
            self.view.show_message("Успех", Messages.ADD_SUCCESS.value)
        except Exception as e:
            self.view.show_message("Ошибка", Messages.ADD_ERROR.value.format(str(e)), is_error=True)

    def search_products(self, criteria: dict) -> list:
        """Search products by criteria."""
        try:
            return self.model.search(**criteria)
        except Exception as e:
            self.view.show_message("Ошибка", Messages.SEARCH_ERROR.value.format(str(e)), is_error=True)
            return []

    def delete_products(self, criteria: dict) -> int:
        """Delete products by criteria."""
        try:
            return self.model.delete_by_criteria(**criteria)
        except Exception as e:
            self.view.show_message("Ошибка", Messages.DELETE_ERROR.value.format(str(e)), is_error=True)
            return 0

    def show_add_dialog(self):
        """Show add product dialog."""
        dialog = AddProductDialog(self.view.root, self)
        self.view.root.wait_window(dialog.dialog)

        if dialog.result:
            self.add_product(dialog.result)

    def show_search_dialog(self):
        """Show search dialog."""
        SearchDialog(self.view.root, self)

    def show_delete_dialog(self):
        """Show delete dialog."""
        DeleteDialog(self.view.root, self)

    # Pagination
    def first_page(self):
        """Go to first page."""
        self.model.set_current_page(1)

    def previous_page(self):
        """Go to previous page."""
        self.model.set_current_page(self.model.current_page - 1)

    def next_page(self):
        """Go to next page."""
        self.model.set_current_page(self.model.current_page + 1)

    def last_page(self):
        """Go to last page."""
        self.model.set_current_page(self.model.total_pages)

    def go_to_page(self):
        """Go to specified page."""
        try:
            page = int(self.view.current_page_var.get())
            self.model.set_current_page(page)
        except ValueError:
            self._update_view()  # Reset to current page

    def change_rows_per_page(self):
        """Change number of rows per page."""
        self.model.get_page(rows_per_page=self.view.rows_per_page_var.get())
        self._update_view()

    def save_to_file(self):
        """Save data to file."""
        if self.file_controller:
            self.file_controller.save_to_file(self.model.products)

    def load_from_file(self):
        """Load data from file."""
        if self.file_controller:
            products = self.file_controller.load_from_file()
            if products:
                self.model.clear()
                self.model.add_products(products)

    # Other
    def show_about(self):
        """Show about dialog."""
        messagebox.showinfo("О программе",
                           "Система управления товарами\n"
                           "Версия 1.0\n\n"
                           "Разработано для управления складскими запасами\n"
                           "с поддержкой поиска и удаления по критериям.")

    def exit_app(self):
        """Exit the application."""
        if self.view.ask_yes_no("Выход", Messages.CONFIRM_EXIT.value):
            self.view.quit()

            @property
            def model(self):
                """Get the model."""
                return self._model