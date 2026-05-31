import xml.sax
from typing import List
from models.product import Product


class ProductHandler(xml.sax.ContentHandler):
    """SAX handler for parsing product XML."""

    def __init__(self):
        self.products = []
        self.current_product = {}
        self.current_tag = ""
        self.current_value = ""

    def startElement(self, tag, attributes):
        """Handle start of an element."""
        self.current_tag = tag
        if tag == "product":
            self.current_product = {}

    def endElement(self, tag):
        """Handle end of an element."""
        if tag == "product":
            try:
                product = Product.from_dict(self.current_product)
                self.products.append(product)
            except (KeyError, ValueError) as e:
                print(f"Error creating product: {e}")
        elif self.current_tag and self.current_value:
            self.current_product[self.current_tag] = self.current_value.strip()

        self.current_tag = ""
        self.current_value = ""

    def characters(self, content):
        """Handle character data."""
        if self.current_tag:
            self.current_value += content


class XMLReader:
    """Reads product data from XML file using SAX parser."""

    @staticmethod
    def read_from_file(filename: str) -> List[Product]:
        """Read products from XML file."""
        handler = ProductHandler()

        try:
            xml.sax.parse(filename, handler)
        except xml.sax.SAXException as e:
            raise ValueError(f"Invalid XML format: {e}")
        except Exception as e:
            raise IOError(f"Error reading file: {e}")

        return handler.products
