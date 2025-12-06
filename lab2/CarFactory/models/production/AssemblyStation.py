from config import constants

class AssemblyStation:
    """Упрощенная сборочная станция"""

    def __init__(self, stationIdentifier: str, stationType: str):
        self._stationIdentifier = stationIdentifier
        self._stationType = stationType
        self._partsCount = constants.ZERO_VALUE

    def addPart(self):
        """Добавить деталь"""
        self._partsCount += constants.ZERO_VALUE + 1
        return True

    def assemble(self):
        """Собрать детали"""

        return self._partsCount > constants.ZERO_VALUE
