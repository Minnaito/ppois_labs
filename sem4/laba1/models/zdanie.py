from datetime import datetime
from typing import List, Dict
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from exceptions.exceptions import ValidationError
from constants import Constants


class zdanie(objekt_nedvizhimosti):
    """Здание."""

    def __init__(self, kolichestvo_etazhej: int, material_sten: str,
                 naznachenie: str, god_postrojki: int,
                 pozharnaya_bezopasnost: str = "не указано",
                 energeticheskaya_effektivnost: str = "не указано",
                 **kwargs):
        super().__init__(**kwargs)
        self._kolichestvo_etazhej = kolichestvo_etazhej
        self._material_sten = material_sten
        self._naznachenie = naznachenie
        self._god_postrojki = god_postrojki
        self._pozharnaya_bezopasnost = pozharnaya_bezopasnost
        self._energeticheskaya_effektivnost = energeticheskaya_effektivnost
        self._poetazhnyj_plan: Dict[int, List[Dict]] = {}
        self._fizicheskij_iznos: int = Constants.MIN_DEPRECIATION
        self._inventarnaya_stoimost: float = Constants.MIN_SHARE

    @property
    def kolichestvo_etazhej(self) -> int:
        return self._kolichestvo_etazhej

    @kolichestvo_etazhej.setter
    def kolichestvo_etazhej(self, value: int) -> None:
        if value <= 0:
            raise ValidationError("Количество этажей должно быть положительным")
        self._kolichestvo_etazhej = value

    @property
    def material_sten(self) -> str:
        return self._material_sten

    @material_sten.setter
    def material_sten(self, value: str) -> None:
        if not value:
            raise ValidationError("Материал стен не может быть пустым")
        self._material_sten = value

    @property
    def naznachenie(self) -> str:
        return self._naznachenie

    @naznachenie.setter
    def naznachenie(self, value: str) -> None:
        allowed = {"zhiloe", "nezhiloe"}
        if value not in allowed:
            raise ValidationError(f"Назначение должно быть одним из {allowed}")
        self._naznachenie = value

    @property
    def god_postrojki(self) -> int:
        return self._god_postrojki

    @god_postrojki.setter
    def god_postrojki(self, value: int) -> None:
        current_year = datetime.now().year
        if value < 1800 or value > current_year:
            raise ValidationError(f"Год постройки должен быть между 1800 и {current_year}")
        self._god_postrojki = value

    @property
    def fizicheskij_iznos(self) -> int:
        return self._fizicheskij_iznos

    @fizicheskij_iznos.setter
    def fizicheskij_iznos(self, value: int) -> None:
        if not (Constants.MIN_DEPRECIATION <= value <= Constants.MAX_DEPRECIATION):
            raise ValidationError("Физический износ должен быть от 0 до 100%")
        self._fizicheskij_iznos = value

    @property
    def pozharnaya_bezopasnost(self) -> str:
        return self._pozharnaya_bezopasnost

    @property
    def energeticheskaya_effektivnost(self) -> str:
        return self._energeticheskaya_effektivnost

    @pozharnaya_bezopasnost.setter
    def pozharnaya_bezopasnost(self, value: str) -> None:
        """Сеттер для пожарной безопасности"""
        self._pozharnaya_bezopasnost = value

    @energeticheskaya_effektivnost.setter
    def energeticheskaya_effektivnost(self, value: str) -> None:
        """Сеттер для энергоэффективности"""
        self._energeticheskaya_effektivnost = value