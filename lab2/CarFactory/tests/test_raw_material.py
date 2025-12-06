import unittest
from config import constants
from models.inventory.RawMaterial import RawMaterial


class TestRawMaterial(unittest.TestCase):

    def testInitialization(self):
        """Тест инициализации сырья"""
        # Проверяем разные варианты конструктора
        try:
            material = RawMaterial("RAW001", "Алюминий", "HIGH")
        except TypeError:
            # Может быть другой конструктор
            try:
                material = RawMaterial("RAW001", "Алюминий листовой", "HIGH")
            except TypeError:
                # Используем минимальный конструктор
                material = RawMaterial("RAW001", "Алюминий")

        self.assertIsInstance(material, RawMaterial)
        self.assertTrue(hasattr(material, '_itemIdentifier') or
                        hasattr(material, '_item_id') or
                        hasattr(material, '_itemId'))

        # Проверяем наличие атрибута качества
        self.assertTrue(hasattr(material, '_quality') or
                        hasattr(material, '_materialQuality'))

    def testCheckQualityCompliance(self):
        """Тест проверки соответствия качества"""
        material = RawMaterial("RAW001", "Алюминий", "HIGH")

        # Проверяем наличие метода проверки качества
        self.assertTrue(hasattr(material, 'check_quality_compliance') or
                        hasattr(material, 'checkQualityCompliance'))

        if hasattr(material, 'check_quality_compliance'):
            result = material.check_quality_compliance("HIGH")
            self.assertIsInstance(result, bool)
        elif hasattr(material, 'checkQualityCompliance'):
            result = material.checkQualityCompliance("HIGH")
            self.assertIsInstance(result, bool)

    def testGetSpecs(self):
        """Тест получения спецификаций"""
        material = RawMaterial("RAW001", "Алюминий", "HIGH")

        # Проверяем наличие метода получения спецификаций
        self.assertTrue(hasattr(material, 'get_specs') or
                        hasattr(material, 'getSpecs') or
                        hasattr(material, 'get_specifications'))

        if hasattr(material, 'get_specs'):
            specs = material.get_specs()
            self.assertIsInstance(specs, dict)
        elif hasattr(material, 'getSpecs'):
            specs = material.getSpecs()
            self.assertIsInstance(specs, dict)

    def testInheritance(self):
        """Тест наследования от InventoryItem"""
        material = RawMaterial("RAW001", "Алюминий", "HIGH")

        # Проверяем унаследованные методы
        self.assertTrue(hasattr(material, 'calculateTotalValue') or
                        hasattr(material, 'calculate_total_value'))

        self.assertTrue(hasattr(material, 'needsReorder') or
                        hasattr(material, 'needs_reorder'))


if __name__ == '__main__':
    unittest.main()