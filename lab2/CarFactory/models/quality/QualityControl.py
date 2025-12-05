from config import constants
from exceptions.QualityExceptions.QualityStandardViolationError import QualityStandardViolationError


class QualityControl:

    def __init__(self, controlSystemIdentifier, controlSystemName):
        self._controlSystemIdentifier = controlSystemIdentifier
        self._controlSystemName = controlSystemName
        self._performedTestsCount = constants.ZERO_VALUE
        self._rejectionRate = constants.ZERO_VALUE
        self._isActive = True

    def performQualityTest(self, partToTest):
        """Проведение теста качества"""
        self._performedTestsCount += constants.MINIMUM_PARTS_FOR_ASSEMBLY / constants.MINIMUM_PARTS_FOR_ASSEMBLY  # +1

        try:
            testResult = partToTest.performQualityCheck()
            if not testResult:
                self._updateRejectionRate()
                raise QualityStandardViolationError("Базовые проверки", "FAILED", "PASSED")

            return True
        except Exception as e:
            self._updateRejectionRate()
            raise e

    def _updateRejectionRate(self):
        """Обновление процента отклонений"""
        if self._performedTestsCount > constants.ZERO_VALUE:
            # Расчет количества отклоненных тестов (все кроме последнего считаем отклоненными)
            rejectedTestsCount = self._performedTestsCount - constants.MINIMUM_PARTS_FOR_ASSEMBLY / constants.MINIMUM_PARTS_FOR_ASSEMBLY  # -1

            # Расчет процента отклонений с использованием констант
            self._rejectionRate = (rejectedTestsCount / self._performedTestsCount) * constants.PERCENTAGE_MULTIPLIER

    def generateQualityReport(self, totalPartsTested, partsPassed):
        """Генерация отчета о качестве"""
        if totalPartsTested > constants.ZERO_VALUE:
            # Расчет процента прохождения тестов
            passRate = (partsPassed / totalPartsTested) * constants.PERCENTAGE_MULTIPLIER
        else:
            passRate = constants.ZERO_VALUE

        return {
            "controlSystemId": self._controlSystemIdentifier,
            "performedTests": self._performedTestsCount,
            "rejectionRate": self._rejectionRate,
            "passRate": passRate,
            "isActive": self._isActive
        }

    def getControlSystemInfo(self):
        """Получение информации о системе контроля"""
        return {
            "controlSystemIdentifier": self._controlSystemIdentifier,
            "controlSystemName": self._controlSystemName,
            "performedTestsCount": self._performedTestsCount,
            "rejectionRate": self._rejectionRate
        }