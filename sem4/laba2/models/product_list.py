from typing import List, Optional, Callable
from .product import Product


class ProductList:
    """Manages a collection of products with pagination."""

    def __init__(self):
        self._products: List[Product] = []
        self._observers: List[Callable] = []
        self._current_page = 1
        self._rows_per_page = 10

    def add_observer(self, observer: Callable) -> None:
        """Add an observer to be notified of changes."""
        self._observers.append(observer)

    def remove_observer(self, observer: Callable) -> None:
        """Remove an observer."""
        if observer in self._observers:
            self._observers.remove(observer)

    def _notify_observers(self) -> None:
        """Notify all observers of changes."""
        for observer in self._observers:
            observer()

    def add_product(self, product: Product) -> None:
        """Add a new product."""
        self._products.append(product)
        self._notify_observers()

    def add_products(self, products: List[Product]) -> None:
        """Add multiple products."""
        self._products.extend(products)
        self._notify_observers()

    def remove_product(self, index: int) -> None:
        """Remove a product by index."""
        if 0 <= index < len(self._products):
            del self._products[index]
            self._notify_observers()

    def clear(self) -> None:
        """Remove all products."""
        self._products.clear()
        self._current_page = 1
        self._notify_observers()

    def search(self, **criteria) -> List[Product]:
        """Search products by criteria."""
        results = []

        for product in self._products:
            match = True

            for key, value in criteria.items():
                if not value:
                    continue

                if key == 'product_name':
                    if value.lower() not in product.product_name.lower():
                        match = False
                        break
                elif key == 'manufacturer_name':
                    if value.lower() not in product.manufacturer_name.lower():
                        match = False
                        break
                elif key == 'manufacturer_unp':
                    if value != product.manufacturer_unp:
                        match = False
                        break
                elif key == 'stock_quantity':
                    try:
                        quantity = int(value)
                        if product.stock_quantity != quantity:
                            match = False
                            break
                    except ValueError:
                        if value.lower() == 'нет на складе' and product.stock_quantity != 0:
                            match = False
                            break
                elif key == 'warehouse_address':
                    if value.lower() not in product.warehouse_address.lower():
                        match = False
                        break

            if match:
                results.append(product)

        return results

    def delete_by_criteria(self, **criteria) -> int:
        """Delete products by criteria."""
        initial_count = len(self._products)
        self._products = [p for p in self._products if not self._matches_criteria(p, **criteria)]
        deleted_count = initial_count - len(self._products)

        if deleted_count > 0:
            self._notify_observers()

        return deleted_count

    def _matches_criteria(self, product: Product, **criteria) -> bool:
        """Check if product matches all criteria."""
        for key, value in criteria.items():
            if not value:
                continue

            if key == 'product_name':
                if value.lower() in product.product_name.lower():
                    return True
            elif key == 'manufacturer_name':
                if value.lower() in product.manufacturer_name.lower():
                    return True
            elif key == 'manufacturer_unp':
                if value == product.manufacturer_unp:
                    return True
            elif key == 'stock_quantity':
                try:
                    quantity = int(value)
                    if product.stock_quantity == quantity:
                        return True
                except ValueError:
                    if value.lower() == 'нет на складе' and product.stock_quantity == 0:
                        return True
            elif key == 'warehouse_address':
                if value.lower() in product.warehouse_address.lower():
                    return True

        return False

    def get_page(self, page: int = None, rows_per_page: int = None) -> List[Product]:
        """Get a page of products."""
        if page is not None:
            self._current_page = max(1, min(page, self.total_pages))

        if rows_per_page is not None:
            self._rows_per_page = rows_per_page
            self._current_page = 1

        start = (self._current_page - 1) * self._rows_per_page
        end = start + self._rows_per_page

        return self._products[start:end]

    @property
    def products(self) -> List[Product]:
        """Get all products."""
        return self._products.copy()

    @property
    def total_count(self) -> int:
        """Get total number of products."""
        return len(self._products)

    @property
    def total_pages(self) -> int:
        """Get total number of pages."""
        return max(1, (len(self._products) + self._rows_per_page - 1) // self._rows_per_page)

    @property
    def current_page(self) -> int:
        """Get current page number."""
        return self._current_page

    @property
    def rows_per_page(self) -> int:
        """Get rows per page."""
        return self._rows_per_page

    def set_current_page(self, page: int) -> None:
        """Set current page."""
        self._current_page = max(1, min(page, self.total_pages))
        self._notify_observers()
