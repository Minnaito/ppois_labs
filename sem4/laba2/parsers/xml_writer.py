import xml.dom.minidom as minidom
from xml.dom.minidom import Document
from typing import List
from models.product import Product


class XMLWriter:
    """Writes product data to XML file using DOM parser."""

    @staticmethod
    def write_to_file(products: List[Product], filename: str) -> None:
        """Write products to XML file."""
        doc = Document()

        root = doc.createElement('products')
        doc.appendChild(root)

        for product in products:
            product_elem = doc.createElement('product')

            XMLWriter._add_element(doc, product_elem, 'product_name', product.product_name)
            XMLWriter._add_element(doc, product_elem, 'manufacturer_name', product.manufacturer_name)
            XMLWriter._add_element(doc, product_elem, 'manufacturer_unp', product.manufacturer_unp)
            XMLWriter._add_element(doc, product_elem, 'stock_quantity', str(product.stock_quantity))
            XMLWriter._add_element(doc, product_elem, 'warehouse_address', product.warehouse_address)

            root.appendChild(product_elem)

        with open(filename, 'w', encoding='utf-8') as f:
            f.write(doc.toprettyxml(indent='  '))

    @staticmethod
    def _add_element(doc: Document, parent, tag_name: str, text: str) -> None:
        """Add an element with text to parent."""
        elem = doc.createElement(tag_name)
        text_node = doc.createTextNode(text)
        elem.appendChild(text_node)
        parent.appendChild(elem)
