import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.inventory.RawMaterial import RawMaterial
from config import constants


class TestRawMaterial(unittest.TestCase):
    """Тесты для класса RawMaterial"""

    def setUp(self):
        """Настройка тестового окружения"""
        self.raw_material = RawMaterial(
            itemIdentifier="RM001",
            itemName="Premium Wheat Flour",
            materialType="FLOUR",
            unitPrice=25.0,
            qualityGrade="PREMIUM"
        )

    def test_raw_material_initialization(self):
        """Тест инициализации сырья"""
        self.assertEqual(self.raw_material._itemIdentifier, "RM001")
        self.assertEqual(self.raw_material._itemName, "Premium Wheat Flour")
        self.assertEqual(self.raw_material._materialType, "FLOUR")
        self.assertEqual(self.raw_material._qualityGrade, "PREMIUM")
        self.assertEqual(self.raw_material._itemType, "RAW_MATERIAL")
        self.assertEqual(self.raw_material._unitPrice, 25.0)
        self.assertIsNone(self.raw_material._expirationDate)

    def test_check_quality_compliance(self):
        """Тест проверки соответствия качества"""
        # Премиум соответствует премиум
        self.assertTrue(self.raw_material.checkQualityCompliance("PREMIUM"))
        # Премиум соответствует высокому
        self.assertTrue(self.raw_material.checkQualityCompliance("HIGH"))
        # Премиум соответствует среднему
        self.assertTrue(self.raw_material.checkQualityCompliance("MEDIUM"))
        # Премиум соответствует низкому
        self.assertTrue(self.raw_material.checkQualityCompliance("LOW"))

        # Средний не соответствует премиум
        medium_material = RawMaterial("RM002", "Standard Flour", "FLOUR", 15.0, "MEDIUM")
        self.assertFalse(medium_material.checkQualityCompliance("PREMIUM"))

    def test_calculate_material_yield(self):
        """Тест расчета выхода материала"""
        yield_percentage = self.raw_material.calculateMaterialYield(
            inputMaterialAmount=100.0,
            outputProductAmount=85.0
        )

        expected_yield = (85.0 / 100.0) * constants.PERCENTAGE_MULTIPLIER
        self.assertEqual(yield_percentage, expected_yield)

    def test_calculate_material_yield_zero_input(self):
        """Тест расчета выхода при нулевом вводе"""
        yield_percentage = self.raw_material.calculateMaterialYield(
            inputMaterialAmount=0.0,
            outputProductAmount=85.0
        )

        self.assertEqual(yield_percentage, constants.ZERO_VALUE)

    def test_set_storage_temperature(self):
        """Тест установки температуры хранения"""
        self.raw_material.setStorageTemperature("15-20°C")
        self.assertEqual(self.raw_material._storageTemperature, "15-20°C")

    def test_set_batch_number(self):
        """Тест установки номера партии"""
        self.raw_material.setBatchNumber("BATCH2024-001")
        self.assertEqual(self.raw_material._batchNumber, "BATCH2024-001")

    def test_add_material_specification(self):
        """Тест добавления спецификации материала"""
        self.raw_material.addMaterialSpecification("ProteinContent", "12%")
        self.raw_material.addMaterialSpecification("Moisture", "14%")

        specifications = self.raw_material._materialSpecifications
        self.assertEqual(specifications["ProteinContent"], "12%")
        self.assertEqual(specifications["Moisture"], "14%")
        self.assertEqual(len(specifications), 2)

    def test_get_material_specifications(self):
        """Тест получения спецификаций материала"""
        self.raw_material.setStorageTemperature("15-20°C")
        self.raw_material.setBatchNumber("BATCH2024-001")
        self.raw_material.addMaterialSpecification("ProteinContent", "12%")

        specifications = self.raw_material.getMaterialSpecifications()

        self.assertEqual(specifications["itemIdentifier"], "RM001")
        self.assertEqual(specifications["materialType"], "FLOUR")
        self.assertEqual(specifications["qualityGrade"], "PREMIUM")
        self.assertEqual(specifications["storageTemperature"], "15-20°C")
        self.assertEqual(specifications["batchNumber"], "BATCH2024-001")
        self.assertEqual(specifications["specificationsCount"], 1)

    def test_is_material_expired(self):
        """Тест проверки истечения срока годности"""
        # Без установленной даты истечения
        self.assertFalse(self.raw_material.isMaterialExpired("2024-12-31"))

        # С установленной датой истечения
        self.raw_material._expirationDate = "2024-06-30"
        self.assertTrue(self.raw_material.isMaterialExpired("2024-12-31"))
        self.assertFalse(self.raw_material.isMaterialExpired("2024-03-15"))


if __name__ == '__main__':
    unittest.main()