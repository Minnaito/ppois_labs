import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from exceptions.QualityExceptions.DefectivePartError import DefectivePartError


class TestDefectivePartError(unittest.TestCase):
    """Тесты для исключения бракованной детали"""

    def testDefectivePartError(self):
        with self.assertRaises(DefectivePartError) as context:
            raise DefectivePartError("PART001", ["трещина", "скол"])

        self.assertIn("Деталь PART001 имеет дефекты", str(context.exception))


if __name__ == '__main__':
    unittest.main()