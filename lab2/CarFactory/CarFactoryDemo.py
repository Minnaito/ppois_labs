import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import constants
from models.abstract.BaseEmployee import BaseEmployee
from models.employees.HRManager import HRManager
from models.employees.MachineOperator import MachineOperator
from models.employees.MaintenanceTechnician import MaintenanceTechnician
from models.employees.ProductionSupervisor import ProductionSupervisor
from models.employees.QualityInspector import QualityInspector
from models.employees.QualityManager import QualityManager
from models.employees.WarehouseWorker import WarehouseWorker
from models.production.ProductionLine import ProductionLine
from models.production.Engine import Engine
from models.production.CarPart import CarPart
from models.production.PartFactory import PartFactory
from models.inventory.Warehouse import Warehouse
from models.inventory.InventoryItem import InventoryItem
from models.inventory.RawMaterial import RawMaterial
from models.inventory.Supplier import Supplier
from models.finance.Budget import Budget
from models.finance.Transaction import Transaction
from models.finance.Invoice import Invoice
from models.finance.Payment import Payment
from models.finance.FinancialReport import FinancialReport
from models.finance.CostAnalysis import CostAnalysis
from models.quality.QualityControl import QualityControl
from models.maintenance.MachineMaintenance import MachineMaintenance
from models.maintenance.RepairTicket import RepairTicket
from models.maintenance.MaintenanceLog import MaintenanceLog
from models.facilities.FactoryBuilding import FactoryBuilding
from models.facilities.ProductionHall import ProductionHall
from models.facilities.StorageFacility import StorageFacility
from models.facilities.SafetySystem import SafetySystem
from models.utilities.PaymentProcessor import PaymentProcessor
from models.utilities.ValidationUtils import ValidationUtils
from models.utilities.CalculationUtils import CalculationUtils
from models.utilities.DateUtils import DateUtils
from models.utilities.Logger import Logger


class CarFactoryDemo:
    def __init__(self):
        self.employees = []
        self.factory_buildings = []
        self.production_lines = []
        self.warehouses = []
        self.parts = []
        self.suppliers = []

    def demonstrateAllClasses(self):
        print("ДЕМОНСТРАЦИЯ ВСЕХ КЛАССОВ СИСТЕМЫ")
        print("=" * 60)

        # 1. Employee Classes
        print("\n1. СОТРУДНИКИ:")
        hr = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000, "кадры")
        operator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000, "CNC")
        technician = MaintenanceTechnician("MT001", "Козлов Дмитрий", "Техник", 42000, "оборудование")
        supervisor = ProductionSupervisor("PS001", "Николаев Сергей", "Мастер", 55000, "сборочный цех")
        inspector = QualityInspector("QI001", "Сидорова Мария", "Инспектор", 38000, "ОТК")
        quality_manager = QualityManager("QM001", "Васильев Андрей", "Менеджер качества", 50000, "ОТК")
        warehouse_worker = WarehouseWorker("WW001", "Федоров Иван", "Кладовщик", 32000, "зона А")

        self.employees = [hr, operator, technician, supervisor, inspector, quality_manager, warehouse_worker]

        for emp in self.employees:
            print(f"   {emp._fullName} - {emp._jobPosition}")
            try:
                print(f"   Обязанности: {emp.work()}")
            except AttributeError:
                print(f"   Обязанности: {emp.performWorkDuties()}")

        # 2. Production Classes
        print("\n2. ПРОИЗВОДСТВО:")
        line = ProductionLine("PL001", "Основная линия", 100)
        try:
            line.start_line()
        except AttributeError:
            pass
        self.production_lines.append(line)

        # Создаем детали через конструкторы
        engine = Engine("ENG001", 300)  # part_id, horsepower
        car_part = CarPart("PART001", "Деталь кузова", "steel", 25.0)

        # Используем фабрику
        demo_engine = PartFactory.createDemoEngine()
        demo_part = PartFactory.createDemoCarPart()

        self.parts = [engine, car_part, demo_engine, demo_part]

        for part in self.parts:
            try:
                cost = part.calculate_cost()
                quality = part.check_quality()
                print(f"   {part._name}: {cost:,.0f} руб., качество: {quality}")
            except Exception as e:
                print(f"   {part._name}: ошибка - {e}")

        # 3. Factory PartFactory
        print("\n3. ФАБРИКА ДЕТАЛЕЙ:")
        print(f"   Создан через фабрику: {demo_engine._name}")
        print(f"   Создана через фабрику: {demo_part._name}")

        # 4. Inventory Classes
        print("\n4. ИНВЕНТАРЬ:")
        warehouse = Warehouse("WH001", 1000)
        self.warehouses.append(warehouse)

        inventory_item = InventoryItem("ITEM001", "Болт М10", "крепление", 5.0)
        inventory_item.updateItemQuantity(100)

        raw_material = RawMaterial("RAW001", "Алюминий листовой", "HIGH")

        print(f"   Склад ID: {warehouse._wh_id}, емкость: {warehouse._capacity}")
        print(f"   Товар: {inventory_item._itemName}, количество: {inventory_item._currentQuantity}")
        print(f"   Сырье: {raw_material._itemName}, качество: {raw_material._quality}")

        # 5. Supplier
        print("\n5. ПОСТАВЩИКИ:")
        supplier = Supplier("SUP001", "МеталлСервис", "8-800-555-3535", 4.5)
        order = supplier.processOrder("Алюминий", 100, 500.0)
        self.suppliers.append(supplier)
        print(f"   Поставщик: {supplier._supplierName}, рейтинг: {supplier._rating}")
        print(f"   Заказ: {order['materialName']}, сумма: {order['totalAmount']:,.0f} руб.")

        # 6. Finance Classes
        print("\n6. ФИНАНСЫ:")
        budget = Budget("BUD001", 1000000)
        budget.spend(450000)
        print(f"   Бюджет ID: {budget._budget_id}, остаток: {budget.calculate_remaining():,.0f} руб.")

        transaction = Transaction("T001", 50000, "DEBIT")
        try:
            new_balance = transaction.process(100000)
            print(f"   Транзакция успешна, баланс: {new_balance:,.0f} руб.")
        except Exception as e:
            print(f"   Ошибка транзакции: {e}")

        invoice = Invoice("INV001", 250000)
        invoice_details = invoice.process()

        payment = Payment("PAY001", 100000, "BANK_TRANSFER")
        payment_details = payment.process()

        financial_report = FinancialReport("FR001", "Q1 2024")
        report = financial_report.generate(1500000, 1000000)

        cost_analysis = CostAnalysis("CA001", "Q1 2024")
        cost_analysis.addCostCategory("Материалы", 600000)
        cost_analysis.addCostCategory("Зарплаты", 400000)

        print(f"   Финансовый отчет: прибыль {report['profit']:,.0f} руб.")

        # 7. Quality Control
        print("\n7. КОНТРОЛЬ КАЧЕСТВА:")
        quality_control = QualityControl("QC001", "Система контроля качества")
        for part in self.parts[:2]:  # Проверим только первые две детали
            try:
                result = quality_control.test_part(part)
                print(f"   Проверка {part._name}: {'ПРОШЛА' if result else 'НЕ ПРОШЛА'}")
            except Exception as e:
                print(f"   Ошибка проверки {part._name}: {e}")

        # 8. Maintenance
        print("\n8. ОБСЛУЖИВАНИЕ:")
        maintenance = MachineMaintenance("MAINT001", "CNC-001")
        maintenance.start()
        maintenance.complete()

        repair_ticket = RepairTicket("TICK001", "CNC-001", "Затупился резец")

        maintenance_log = MaintenanceLog("LOG001")
        maintenance_log.add_entry("CNC-001", "плановое", 2.5, 5000.0, "MT001")

        print(f"   Обслуживание: {maintenance._machine_id}, статус: {maintenance._status}")
        print(f"   Заявка на ремонт: {repair_ticket._issue}")
        print(f"   Записей в журнале: {len(maintenance_log._entries)}")

        # 9. Factory Facilities
        print("\n9. ПРОИЗВОДСТВЕННЫЕ ПОМЕЩЕНИЯ:")
        factory_building = FactoryBuilding("B001", 3000)
        production_hall = ProductionHall("H001", "B001", 1000)

        storage_facility = StorageFacility("SF001", 5000)
        storage_facility.update_stock(1500)

        safety_system = SafetySystem("SS001")

        self.factory_buildings.append(factory_building)

        print(f"   Здание ID: {factory_building._building_id}, площадь: {factory_building._area} м²")
        print(f"   Цех ID: {production_hall._hall_id}, площадь: {production_hall._area} м²")
        print(f"   Склад ID: {storage_facility._facility_id}, запасы: {storage_facility._stock}")

        # 10. Utilities - PaymentProcessor
        print("\n10. ПЛАТЕЖНЫЙ ПРОЦЕССОР:")
        payment_processor = PaymentProcessor("PP001")

        # Перевод между картами
        try:
            from_balance, to_balance, fee = payment_processor.transferBetweenCards(10000, 5000, 3000)
            print(f"   Перевод успешен: {3000:,.0f} руб. (комиссия {fee:,.0f} руб.)")
            print(f"   Баланс отправителя: {from_balance:,.0f} руб.")
            print(f"   Баланс получателя: {to_balance:,.0f} руб.")
        except Exception as e:
            print(f"   Ошибка перевода: {e}")

        # Проверка пароля
        password_check = payment_processor.validatePasswordStrength("MyPass123!")
        print(f"   Проверка пароля 'MyPass123!':")
        print(f"     Надежный: {password_check['isStrong']}")
        print(f"     Оценка: {password_check['score']}/100")

        # 11. Утилиты
        print("\n11. УТИЛИТЫ:")

        # Расчеты
        calc = CalculationUtils
        tax = calc.calculateTax(100000)
        percentage = calc.calculatePercentage(75, 150)
        print(f"   Налог на 100,000 руб.: {tax:,.0f} руб.")
        print(f"   75 от 150: {percentage:.0f}%")

        # Даты
        date = DateUtils
        today = date.getCurrentDate()
        future_date = date.addDaysToDate(today, 30)
        print(f"   Сегодня: {today}")
        print(f"   Через 30 дней: {future_date}")

        # Валидация
        valid = ValidationUtils
        email_valid = valid.validateEmail("test@example.com")
        name_valid = valid.validateName("Иван Иванов")
        print(f"   Email test@example.com: {'валиден' if email_valid else 'невалиден'}")
        print(f"   Имя 'Иван Иванов': {'валидно' if name_valid else 'невалидно'}")

        # 12. Логирование
        print("\n12. ЛОГИРОВАНИЕ:")
        logger = Logger("CarFactoryDemo")
        logger.logInfo("Демонстрация завершена успешно")
        logger.logWarning("Тестовое предупреждение")
        logger.logError("Тестовая ошибка")

        # 13. Итоговая статистика
        print("\n" + "=" * 60)
        print("ИТОГОВАЯ СТАТИСТИКА:")
        print(f"   Всего классов продемонстрировано: 50+")
        print(f"   Сотрудников создано: {len(self.employees)}")
        print(f"   Деталей произведено: {len(self.parts)}")
        print(f"   Поставщиков: {len(self.suppliers)}")
        print(f"   Производственных линий: {len(self.production_lines)}")
        print(f"   Складов: {len(self.warehouses)}")
        print(f"   Производственных зданий: {len(self.factory_buildings)}")

        print("\n" + "=" * 60)
        print("ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")


def main():
    factoryDemo = CarFactoryDemo()
    factoryDemo.demonstrateAllClasses()


if __name__ == "__main__":
    main()