class AssemblyStation:
    """Упрощенная сборочная станция"""

    def __init__(self, stationIdentifier: str, stationType: str):
        self._stationIdentifier = stationIdentifier
        self._stationType = stationType
        self._partsCount = 0  # 3 поля вместо 8

    def addPart(self):
        """Добавить деталь"""
        self._partsCount += 1
        return True

    def assemble(self):
        """Собрать детали"""
        return self._partsCount > 0