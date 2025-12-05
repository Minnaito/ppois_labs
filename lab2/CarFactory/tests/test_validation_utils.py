import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from models.utilities.ValidationUtils import ValidationUtils


class TestValidationUtils(unittest.TestCase):
    """Тесты для утилит валидации"""

    def testValidateEmail(self):
        self.assertTrue(ValidationUtils.validateEmail("test@example.com"))

    def testValidateName(self):
        self.assertTrue(ValidationUtils.validateName("Иван"))


if __name__ == '__main__':
    unittest.main()