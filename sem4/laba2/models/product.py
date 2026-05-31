from datetime import datetime
from typing import Optional
from dataclasses import dataclass


@dataclass
class Product:
    """Represents a product in the inventory."""
    product_name: str
    manufacturer_name: str
    manufacturer_unp: int
    stock_quantity: int
    warehouse_address: str

    def validate(self) -> None:
        """Validate product data."""
        if not self.product_name or not self.product_name.strip():
            raise ValueError("Product name cannot be empty")

        if not self.manufacturer_name or not self.manufacturer_name.strip():
            raise ValueError("Manufacturer name cannot be empty")

        if len(str(self.manufacturer_unp)) != 9:
            raise ValueError("Manufacturer UNP must be 9 digits")

        if not isinstance(self.stock_quantity, int) or self.stock_quantity < 0:
            raise ValueError("Stock quantity must be a non-negative integer")

        if not self.warehouse_address or not self.warehouse_address.strip():
            raise ValueError("Warehouse address cannot be empty")

    def to_dict(self) -> dict:
        """Convert product to dictionary."""
        return {
            'product_name': self.product_name,
            'manufacturer_name': self.manufacturer_name,
            'manufacturer_unp': self.manufacturer_unp,
            'stock_quantity': self.stock_quantity,
            'warehouse_address': self.warehouse_address,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        """Create product from dictionary."""

        return cls(
            product_name=data['product_name'],
            manufacturer_name=data['manufacturer_name'],
            manufacturer_unp=data['manufacturer_unp'],
            stock_quantity=int(data['stock_quantity']),
            warehouse_address=data['warehouse_address'],
        )
