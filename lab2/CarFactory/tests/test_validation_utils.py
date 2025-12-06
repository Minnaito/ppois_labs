import unittest
from config import constants
from models.utilities.ValidationUtils import ValidationUtils


class TestValidationUtils(unittest.TestCase):

    def testValidateEmail(self):
        self.assertTrue(ValidationUtils.validateEmail("test@example.com"))
        self.assertFalse(ValidationUtils.validateEmail("invalid-email"))
        self.assertFalse(ValidationUtils.validateEmail("test@"))
        self.assertFalse(ValidationUtils.validateEmail("@example.com"))

    def testValidatePhone(self):
        # Проверяем российские форматы
        self.assertTrue(ValidationUtils.validatePhone("+79161234567"))
        self.assertTrue(ValidationUtils.validatePhone("89161234567"))
        self.assertFalse(ValidationUtils.validatePhone("12345"))
        self.assertFalse(ValidationUtils.validatePhone("abc"))

    def testValidateName(self):
        self.assertTrue(ValidationUtils.validateName("Иван Иванов"))
        self.assertTrue(ValidationUtils.validateName("John Doe"))
        self.assertTrue(ValidationUtils.validateName("Анна-Мария"))

        # Проверяем минимальную длину (должна быть не менее 2 символов)
        if constants.MINIMUM_NAME_LENGTH == 2:
            self.assertFalse(ValidationUtils.validateName("А"))
            self.assertTrue(ValidationUtils.validateName("Ан"))
        else:
            # Если минимальная длина другая, проверяем соответствующим образом
            min_length = constants.MINIMUM_NAME_LENGTH
            short_name = "А" * (min_length - 1)
            valid_name = "А" * min_length

            self.assertFalse(ValidationUtils.validateName(short_name))
            self.assertTrue(ValidationUtils.validateName(valid_name))

    def testValidateSalary(self):
        self.assertTrue(ValidationUtils.validateSalary(constants.MINIMUM_EMPLOYEE_SALARY))
        self.assertTrue(ValidationUtils.validateSalary(constants.MINIMUM_EMPLOYEE_SALARY + 1000))
        self.assertFalse(ValidationUtils.validateSalary(constants.MINIMUM_EMPLOYEE_SALARY - 1))
        self.assertFalse(ValidationUtils.validateSalary(-1000))

    def testValidateWeight(self):
        self.assertTrue(ValidationUtils.validateWeight(constants.MINIMUM_PART_WEIGHT))
        self.assertTrue(ValidationUtils.validateWeight(constants.MINIMUM_PART_WEIGHT + 1.0))
        self.assertFalse(ValidationUtils.validateWeight(constants.MINIMUM_PART_WEIGHT - 0.1))
        self.assertFalse(ValidationUtils.validateWeight(-1.0))


if __name__ == '__main__':
    unittest.main()