from abc import ABC


class dokument(ABC):
    """Абстрактный класс документа."""

    def __init__(self, nomer_dokumenta: str, data_vydachi: str, organ_vydachi: str):
        self._nomer_dokumenta = nomer_dokumenta
        self._data_vydachi = data_vydachi
        self._organ_vydachi = organ_vydachi

    @property
    def nomer_dokumenta(self) -> str:
        return self._nomer_dokumenta

    @property
    def data_vydachi(self) -> str:
        return self._data_vydachi

    @property
    def organ_vydachi(self) -> str:
        return self._organ_vydachi

