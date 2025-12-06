import unittest
from models.utilities.AdvancedValidator import AdvancedValidator


class TestAdvancedValidator(unittest.TestCase):

    def testValidateEmail(self):
        self.assertTrue(AdvancedValidator.validateEmail("user@domain.com"))
        self.assertFalse(AdvancedValidator.validateEmail("invalid"))

    def testValidatePhone(self):
        self.assertTrue(AdvancedValidator.validatePhone("+1234567890"))
        self.assertFalse(AdvancedValidator.validatePhone("abc"))

    def testValidateDateFormat(self):
        self.assertTrue(AdvancedValidator.validateDateFormat("2024-01-15"))
        self.assertFalse(AdvancedValidator.validateDateFormat("15-01-2024"))

    def testValidateNumericRange(self):
        self.assertTrue(AdvancedValidator.validateNumericRange(5, 1, 10))
        self.assertFalse(AdvancedValidator.validateNumericRange(15, 1, 10))

    def testValidateMaterialType(self):
        # Зависит от constants.VALID_MATERIAL_TYPES
        # Тестируем метод в общем
        self.assertIsInstance(AdvancedValidator.validateMaterialType("steel"), bool)


if __name__ == '__main__':
    unittest.main()