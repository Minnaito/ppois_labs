import unittest
from models.facilities.FactoryBuilding import FactoryBuilding
from models.facilities.ProductionHall import ProductionHall
from models.facilities.StorageFacility import StorageFacility
from models.facilities.SafetySystem import SafetySystem


class TestAllFacilities(unittest.TestCase):

    def testAllFacilities(self):
        building = FactoryBuilding("B001", 3000)
        hall = ProductionHall("H001", "B001", 1000)
        storage = StorageFacility("SF001", 5000)
        safety = SafetySystem("SS001")

        facilities = [building, hall, storage, safety]

        for facility in facilities:
            if hasattr(facility, 'get_info'):
                info = facility.get_info()
                self.assertIsInstance(info, dict)
            elif hasattr(facility, 'get_stats'):
                stats = facility.get_stats()
                self.assertIsInstance(stats, dict)


if __name__ == '__main__':

    unittest.main()
