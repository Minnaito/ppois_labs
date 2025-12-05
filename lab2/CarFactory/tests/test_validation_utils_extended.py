import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.ValidationUtils import ValidationUtils

class TestValidationUtilsExtended(unittest.TestCase):
    """Расширенные тесты для утилит валидации"""

    def testValidateEmail(self):
        self.assertTrue(ValidationUtils.validateEmail("test@example.com"))
        self.assertFalse(ValidationUtils.validateEmail("invalid-email"))

    def testValidatePhone(self):
        self.assertTrue(ValidationUtils.validatePhone("+79123456789"))
        self.assertTrue(ValidationUtils.validatePhone("89123456789"))
        self.assertFalse(ValidationUtils.validatePhone("123"))

    def testValidateName(self):
        self.assertTrue(ValidationUtils.validateName("Иван Иванов"))
        self.assertFalse(ValidationUtils.validateName("А"))  # Слишком короткое
        self.assertFalse(ValidationUtils.validateName(""))   # Пустое

    def testValidateSalary(self):
        self.assertTrue(ValidationUtils.validateSalary(30000))
        self.assertTrue(ValidationUtils.validateSalary(0))
        self.assertFalse(ValidationUtils.validateSalary(-1000))

    def testValidateWeight(self):
        self.assertTrue(ValidationUtils.validateWeight(10.5))
        self.assertFalse(ValidationUtils.validateWeight(0.05))  # Меньше минимума

if __name__ == '__main__':
    unittest.main()