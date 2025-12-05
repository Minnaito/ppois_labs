from config import constants
from models.employees.HRManager import HRManager
from models.employees.MachineOperator import MachineOperator
from models.employees.MaintenanceTechnician import MaintenanceTechnician
from models.employees.ProductionSupervisor import ProductionSupervisor
from models.employees.QualityInspector import QualityInspector
from models.employees.WarehouseWorker import WarehouseWorker
from models.production.ProductionLine import ProductionLine
from models.production.Engine import Engine
from models.production.Transmission import Transmission
from models.inventory.Warehouse import Warehouse
from models.finance.Transaction import Transaction
from models.finance.Budget import Budget
from models.quality.QualityControl import QualityControl
from models.maintenance.MachineMaintenance import MachineMaintenance
from models.maintenance.RepairTicket import RepairTicket
from models.facilities.FactoryBuilding import FactoryBuilding


class CarFactoryDemo:
    def __init__(self):
        self.employees = []
        self.productionLines = []
        self.warehouses = []
        self.factoryBuildings = []
        self.totalProduction = 0
        self.financialBalance = 5000000

    def setupBasicInfrastructure(self):
        print("1. СОЗДАНИЕ ИНФРАСТРУКТУРЫ")

        factoryBuilding = FactoryBuilding("B001", "Главный корпус", 3000, 2020, "Производственный")
        self.factoryBuildings.append(factoryBuilding)
        print("   Создано производственное здание")

        hrManager = HRManager("HR001", "Иванова Анна", "HR менеджер", 45000, "кадры")
        machineOperator = MachineOperator("OP001", "Петров Алексей", "Оператор", 35000, "CNC")
        qualityInspector = QualityInspector("QI001", "Сидорова Мария", "Инспектор", 38000, "ОТК")
        maintenanceTechnician = MaintenanceTechnician("MT001", "Козлов Дмитрий", "Техник", 42000, "оборудование")
        productionSupervisor = ProductionSupervisor("PS001", "Николаев Сергей", "Мастер", 55000, "сборочный цех")
        warehouseWorker = WarehouseWorker("WW001", "Федоров Иван", "Кладовщик", 32000, "зона А")

        self.employees.extend(
            [hrManager, machineOperator, qualityInspector, maintenanceTechnician, productionSupervisor,
             warehouseWorker])

        monthly_salary_fund = sum(getattr(emp, '_monthlySalary', 0) for emp in self.employees)
        print(f"   Нанято сотрудников: {len(self.employees)}")
        print(f"   Месячный фонд зарплаты: {monthly_salary_fund:,.0f} руб.")
        print(f"   Средняя зарплата: {monthly_salary_fund / len(self.employees):,.0f} руб./мес")

        productionLine = ProductionLine("PL001", "Основная линия", 400)
        productionLine.startProductionLine()
        self.productionLines.append(productionLine)
        print("   Запущена производственная линия")

        warehouse = Warehouse(
            "WH001",
            "Основной склад",
            constants.DEFAULT_WAREHOUSE_CAPACITY,
            "корпус Б"
        )
        self.warehouses.append(warehouse)
        print(f"   Создан склад (емкость: {constants.DEFAULT_WAREHOUSE_CAPACITY} ед.)")

    def demonstrateEmployeeWork(self):
        print("\n2. РАБОТА СОТРУДНИКОВ")

        total_monthly_salary = 0

        for employee in self.employees:
            try:
                employeeInfo = employee.getEmployeeInfo()
                employeeName = employeeInfo.get('fullName', 'Неизвестный сотрудник')
                jobPosition = employeeInfo.get('jobPosition', 'Должность не указана')
                monthlySalary = employeeInfo.get('monthlySalary', 0)
            except:
                employeeName = getattr(employee, '_fullName', 'Неизвестный сотрудник')
                jobPosition = getattr(employee, '_jobPosition', 'Должность не указана')
                monthlySalary = getattr(employee, '_monthlySalary', 0)

            total_monthly_salary += monthlySalary

            print(f"   {employeeName} - {jobPosition}")

            if hasattr(employee, 'performWorkDuties'):
                duties = employee.performWorkDuties()
                print(f"   Обязанности: {duties}")

            annualSalary = monthlySalary * 12
            print(f"   Годовая зарплата: {annualSalary:,.0f} руб.")
            print()

        print(f"   ИТОГО по персоналу:")
        print(f"     Сотрудников: {len(self.employees)}")
        print(f"     Месячный фонд зарплат: {total_monthly_salary:,.0f} руб.")
        print(f"     Годовой фонд зарплат: {total_monthly_salary * 12:,.0f} руб.")

    def demonstrateProduction(self):
        print("\n3. ПРОИЗВОДСТВЕННЫЙ ПРОЦЕСС")

        production_capacity = 400
        utilization_rate = 0.75

        engine_batch_size = int(production_capacity * utilization_rate * 0.6)
        print(f"   Производство партии из {engine_batch_size} двигателей...")

        engine = Engine(
            "ENG001", "Двигатель V6", "алюминий", constants.DEMO_ENGINE_WEIGHT,
            constants.DEMO_ENGINE_HORSEPOWER, constants.DEMO_ENGINE_CYLINDERS, "бензин"
        )
        engineCost = engine.calculateProductionCost()
        engineSpecs = engine.getEngineSpecifications()

        print(f"   Произведен образец: {engine.partName}")
        print(f"     Стоимость производства: {engineCost:,.0f} руб.")
        print(f"     Мощность: {engineSpecs['horsepower']} л.с.")
        print(f"     Цилиндров: {engineSpecs['cylinderCount']}")

        transmission_batch_size = int(production_capacity * utilization_rate * 0.4)
        print(f"   Производство партии из {transmission_batch_size} трансмиссий...")

        transmission = Transmission(
            "TRANS001", "6-ступенчатая МКПП", "сталь", 85.0,
            "механическая", 6
        )
        transmissionCost = transmission.calculateProductionCost()

        print(f"   Произведен образец: {transmission.partName}")
        print(f"     Стоимость производства: {transmissionCost:,.0f} руб.")
        print(f"     Передач: {transmission._gearCount}")

        if self.productionLines:
            productionLine = self.productionLines[0]
            total_produced = engine_batch_size + transmission_batch_size
            productionLine._currentProductionCount = total_produced
            productionLine._maximumCapacity = production_capacity
            self.totalProduction = total_produced

            statistics = productionLine.getProductionStatistics()
            print(f"\n   Производственная линия:")
            print(f"     Выпущено за смену: {statistics['currentProduction']} деталей")
            print(f"     Мощность линии: {statistics['maximumCapacity']} деталей/смена")
            print(f"     Загрузка линии: {(statistics['currentProduction'] / statistics['maximumCapacity']) * 100:.1f}%")

            total_engine_cost = engineCost * engine_batch_size
            total_transmission_cost = transmissionCost * transmission_batch_size
            total_production_cost = total_engine_cost + total_transmission_cost
            print(f"     Себестоимость партии: {total_production_cost:,.0f} руб.")
            print(f"     Средняя себестоимость: {total_production_cost / total_produced:,.0f} руб./ед.")

        self.engine_batch_size = engine_batch_size
        self.transmission_batch_size = transmission_batch_size
        self.engineCost = engineCost
        self.transmissionCost = transmissionCost

    def demonstrateWarehouseOperations(self):
        print("\n4. СКЛАДСКИЕ ОПЕРАЦИИ")

        if self.warehouses:
            warehouse = self.warehouses[0]

            materials = [
                ("Двигатель V6", self.totalProduction, 45000),
                ("Коробка передач", self.totalProduction, 28000),
                ("Тормозные диски", 100, 4000),
                ("Алюминиевые заготовки", 200, 1500),
                ("Электронные блоки", 20, 12000)
            ]

            totalValue = 0
            added_items = 0
            for materialName, materialQuantity, materialPrice in materials:
                try:
                    warehouse.addInventoryItem(materialName, materialQuantity, materialPrice)
                    totalValue += materialQuantity * materialPrice
                    added_items += materialQuantity
                    print(f"     Добавлено: {materialName} - {materialQuantity} шт.")
                except Exception as error:
                    print(f"     Ошибка: {materialName} - {error}")

            warehouseStatus = warehouse.getWarehouseStatus()
            print(f"\n   Статус склада:")
            print(f"     Название: {warehouseStatus['warehouseName']}")
            print(f"     Товаров на складе: {warehouseStatus['currentStock']} ед.")
            print(f"     Загруженность склада: {warehouseStatus['utilizationPercentage']:.1f}%")
            print(f"     Общая стоимость запасов: {totalValue:,.0f} руб.")
            print(f"     Добавлено единиц: {added_items}")

    def demonstrateFinancialOperations(self):
        print("\n5. ФИНАНСОВЫЕ ОПЕРАЦИИ")

        monthly_salary_cost = sum(getattr(emp, '_monthlySalary', 0) for emp in self.employees)
        quarterly_salary_cost = monthly_salary_cost * 3

        print(f"   Расчет затрат на персонал:")
        print(f"     Месячный фонд зарплат: {monthly_salary_cost:,.0f} руб.")
        print(f"     Квартальный фонд зарплат: {quarterly_salary_cost:,.0f} руб.")
        print(f"     Годовой фонд зарплат: {monthly_salary_cost * 12:,.0f} руб.")

        total_budget = 7000000
        productionBudget = Budget("BUD001", "Производственный бюджет Q1 2024", total_budget, "Q1 2024")

        salary_budget = quarterly_salary_cost * 1.34

        if salary_budget > total_budget * 0.4:
            salary_budget = total_budget * 0.4

        materials_budget = total_budget * 0.35
        equipment_budget = total_budget * 0.15
        energy_budget = total_budget * 0.05
        overhead_budget = total_budget * 0.05

        print(f"\n   РАСПРЕДЕЛЕНИЕ БЮДЖЕТА:")

        if not productionBudget.allocateFunds("Зарплаты и взносы", salary_budget):
            print(f"     Не удалось выделить {salary_budget:,.0f} руб. на зарплаты")
            salary_budget = total_budget * 0.3
            productionBudget.allocateFunds("Зарплаты и взносы", salary_budget)

        if not productionBudget.allocateFunds("Закупка материалов", materials_budget):
            print(f"     Не удалось выделить {materials_budget:,.0f} руб. на материалы")
            materials_budget = total_budget * 0.3
            productionBudget.allocateFunds("Закупка материалов", materials_budget)

        productionBudget.allocateFunds("Обслуживание оборудования", equipment_budget)
        productionBudget.allocateFunds("Энергоресурсы", energy_budget)
        productionBudget.allocateFunds("Накладные расходы", overhead_budget)

        print(f"     Зарплаты: {salary_budget:,.0f} руб.")
        print(f"     Материалы: {materials_budget:,.0f} руб.")
        print(f"     Оборудование: {equipment_budget:,.0f} руб.")
        print(f"     Энергия: {energy_budget:,.0f} руб.")
        print(f"     Накладные: {overhead_budget:,.0f} руб.")

        print(f"\n   РАСХОДОВАНИЕ СРЕДСТВ:")

        try:
            productionBudget.recordExpense("Зарплаты и взносы", salary_budget)
            print(f"     Зарплаты: {salary_budget:,.0f} руб. (100%)")
        except Exception as e:
            print(f"     Ошибка зарплат: {e}")
            try:
                productionBudget.recordExpense("Зарплаты и взносы", salary_budget * 0.95)
                print(f"     Зарплаты: {salary_budget * 0.95:,.0f} руб. (95%)")
            except:
                print(f"     Невозможно записать расходы на зарплаты")

        engine_cost_per_unit = 45000
        transmission_cost_per_unit = 28000
        engine_count = getattr(self, 'engine_batch_size', 180)
        transmission_count = getattr(self, 'transmission_batch_size', 120)

        materials_needed = (engine_count * engine_cost_per_unit +
                            transmission_count * transmission_cost_per_unit)

        materials_to_spend = min(materials_needed, materials_budget * 0.85)

        try:
            productionBudget.recordExpense("Закупка материалов", materials_to_spend)
            print(f"     Материалы: {materials_to_spend:,.0f} руб. ({materials_to_spend / materials_budget * 100:.1f}%)")
            print(f"       Нужно было: {materials_needed:,.0f} руб.")
        except Exception as e:
            print(f"     Ошибка материалов: {e}")
            try:
                materials_to_spend = materials_budget * 0.7
                productionBudget.recordExpense("Закупка материалов", materials_to_spend)
                print(f"     Материалы: {materials_to_spend:,.0f} руб. (70%)")
            except:
                print(f"     Невозможно записать расходы на материалы")

        for category, budget_amount, percentage in [
            ("Обслуживание оборудования", equipment_budget, 0.6),
            ("Энергоресурсы", energy_budget, 0.8),
            ("Накладные расходы", overhead_budget, 0.7)
        ]:
            try:
                expense_amount = budget_amount * percentage
                productionBudget.recordExpense(category, expense_amount)
                print(f"     {category}: {expense_amount:,.0f} руб. ({percentage * 100:.0f}%)")
            except Exception as e:
                print(f"     {category}: {e}")
                try:
                    expense_amount = budget_amount * (percentage - 0.2)
                    productionBudget.recordExpense(category, expense_amount)
                    print(f"     {category}: {expense_amount:,.0f} руб. ({percentage * 100 - 20:.0f}%)")
                except:
                    print(f"     Невозможно записать расходы на {category}")

        budgetStatus = productionBudget.getBudgetStatus()

        print(f"\n   БЮДЖЕТНЫЙ ОТЧЕТ:")
        print(f"     Бюджет: {budgetStatus['budgetName']}")
        print(f"     Общая сумма: {budgetStatus['totalAmount']:,.0f} руб.")
        print(f"     Распределено: {budgetStatus['allocatedAmount']:,.0f} руб.")
        print(f"     Израсходовано: {budgetStatus['spentAmount']:,.0f} руб.")
        print(f"     Остаток: {budgetStatus['remainingAmount']:,.0f} руб.")
        print(f"     Использование: {budgetStatus['utilizationPercentage']:.1f}%")

        if 'categoryDetails' in budgetStatus:
            print(f"\n   ДЕТАЛИ ПО КАТЕГОРИЯМ:")
            for category, details in budgetStatus['categoryDetails'].items():
                print(f"     {category}:")
                print(f"       Выделено: {details['allocated']:,.0f} руб.")
                print(f"       Израсходовано: {details['spent']:,.0f} руб.")
                print(f"       Остаток: {details['remaining']:,.0f} руб.")
                print(f"       Использование: {details['utilization']:.1f}%")

    def demonstrateQualityControl(self):
        print("\n6. КОНТРОЛЬ КАЧЕСТВА")

        qualityControlSystem = QualityControl("QC001", "Система контроля качества")

        test_parts_count = self.totalProduction
        quality_rate = 0.97
        passed_tests = int(test_parts_count * quality_rate)

        print(f"   Контроль качества произведенной партии...")
        print(f"     Всего деталей: {test_parts_count}")

        qualityReport = qualityControlSystem.generateQualityReport(test_parts_count, passed_tests)

        print(f"\n   ОТЧЕТ ПО КАЧЕСТВУ:")
        print(f"     Система: {qualityControlSystem._controlSystemName}")
        print(f"     Процент прохождения: {qualityReport['passRate']:.1f}%")
        print(f"     Процент брака: {100 - qualityReport['passRate']:.1f}%")

        if qualityReport['passRate'] >= 98:
            print(f"     Качество: ПРЕМИУМ КЛАСС")
        elif qualityReport['passRate'] >= 96:
            print(f"     Качество: ВЫСОКОЕ")
        elif qualityReport['passRate'] >= 94:
            print(f"     Качество: СРЕДНЕЕ")
        else:
            print(f"     Качество: ТРЕБУЕТ УЛУЧШЕНИЯ")

    def demonstrateMaintenance(self):
        print("\n7. ТЕХНИЧЕСКОЕ ОБСЛУЖИВАНИЕ")

        print("   Техническое обслуживание производственного оборудования")

        maintenance_tasks = [
            ("ТО-001", "CNC станок", "Ежемесячное ТО", 3.5, 98),
            ("ТО-002", "Гидравлический пресс", "Замена фильтров", 1.5, 95),
            ("ТО-003", "Сварочный робот", "Калибровка", 2.0, 96),
        ]

        total_hours = 0
        completed = 0

        for task_id, equipment, task_type, hours, success_rate in maintenance_tasks:
            print(f"     {equipment}: {task_type}")
            print(f"       Запланировано: {hours} часов")

            if success_rate >= 95:
                print(f"       Выполнено успешно")
                completed += 1
                total_hours += hours
            else:
                print(f"       Требуется доработка")

        print(f"\n   ИТОГИ ОБСЛУЖИВАНИЯ:")
        print(f"     Выполнено задач: {completed}/{len(maintenance_tasks)}")
        print(f"     Затрачено времени: {total_hours} часов")

    def generateFinalReport(self):
        print("\n8. ИТОГОВЫЙ ОТЧЕТ ПО ПРЕДПРИЯТИЮ")

        totalEmployees = len(self.employees)

        totalAnnualSalary = 0
        for employee in self.employees:
            monthlySalary = getattr(employee, '_monthlySalary', 0)
            totalAnnualSalary += monthlySalary * 12

        averageSalary = totalAnnualSalary / totalEmployees if totalEmployees > 0 else 0

        if self.productionLines:
            statistics = self.productionLines[0].getProductionStatistics()
            production_capacity = statistics['maximumCapacity']
            current_production = statistics['currentProduction']
            production_efficiency = (current_production / production_capacity * 100) if production_capacity > 0 else 0
        else:
            production_capacity = 0
            current_production = 0
            production_efficiency = 0

        if self.warehouses:
            warehouseStatus = self.warehouses[0].getWarehouseStatus()
            warehouse_capacity = warehouseStatus['maximumCapacity']
            current_stock = warehouseStatus['currentStock']
            warehouse_utilization = (current_stock / warehouse_capacity * 100) if warehouse_capacity > 0 else 0
        else:
            warehouse_capacity = 0
            current_stock = 0
            warehouse_utilization = 0

        print("   КЛЮЧЕВЫЕ ПОКАЗАТЕЛИ ПРЕДПРИЯТИЯ:")
        print(f"     ПЕРСОНАЛ: {totalEmployees} чел.")
        print(f"       Годовой ФОТ: {totalAnnualSalary:,.0f} руб.")
        print(f"       Средняя зарплата: {averageSalary:,.0f} руб./мес")
        print()
        print(f"     ПРОИЗВОДСТВО:")
        print(f"       Произведено: {self.totalProduction} ед.")
        print(f"       Мощность: {production_capacity} ед./смена")
        print(f"       Загрузка: {production_efficiency:.1f}%")
        print()
        print(f"     СКЛАДЫ:")
        print(f"       Емкость: {warehouse_capacity} ед.")
        print(f"       Запасы: {current_stock} ед.")
        print(f"       Загрузка: {warehouse_utilization:.1f}%")
        print()
        print(f"     ФИНАНСЫ:")
        print(f"       Баланс: {self.financialBalance:,.0f} руб.")

        print(f"\n   ОЦЕНКА ЭФФЕКТИВНОСТИ:")

        if production_efficiency >= 80:
            print(f"     Производство: Хорошая загрузка")
        elif production_efficiency >= 60:
            print(f"     Производство: Нормальная загрузка")
        else:
            print(f"     Производство: Низкая загрузка")

        if warehouse_utilization >= 60:
            print(f"     Склады: Хорошая загрузка")
        elif warehouse_utilization >= 40:
            print(f"     Склады: Нормальная загрузка")
        else:
            print(f"     Склады: Низкая загрузка")

        if self.financialBalance >= 10000000:
            print(f"     Финансы: Хорошее состояние")
        elif self.financialBalance >= 5000000:
            print(f"     Финансы: Нормальное состояние")
        else:
            print(f"     Финансы: Низкое состояние")

    def runCompleteDemo(self):
        print("ЗАПУСК ДЕМОНСТРАЦИИ АВТОМОБИЛЬНОГО ЗАВОДА")
        print("=" * 60)

        try:
            self.setupBasicInfrastructure()
            self.demonstrateEmployeeWork()
            self.demonstrateProduction()
            self.demonstrateWarehouseOperations()
            self.demonstrateFinancialOperations()
            self.demonstrateQualityControl()
            self.demonstrateMaintenance()
            self.generateFinalReport()

            print("\n" + "=" * 50)
            print("ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА")
            print("=" * 50)

        except Exception as error:
            print(f"\nОШИБКА: {error}")
            import traceback
            traceback.print_exc()
            print("Демонстрация прервана")


def main():
    factoryDemo = CarFactoryDemo()
    factoryDemo.runCompleteDemo()


if __name__ == "__main__":
    main()