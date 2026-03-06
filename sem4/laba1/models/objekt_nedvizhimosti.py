from abc import ABC
from datetime import datetime
from typing import Optional

from models.base_model import base_model
from exceptions.exceptions import ValidationError

class objekt_nedvizhimosti(base_model, ABC):
    def __init__(self, adres: str, ploshchad: float,
                 status: str = "vremennyy",
                 data_registracii: Optional[str] = None,
                 data_poslednego_tekh_ucheta: Optional[str] = None,
                 nomer_tekhpasporta: Optional[str] = None,
                 saved_vypiska: Optional[str] = None,  # новое поле
                 **kwargs):
        super().__init__(**kwargs)
        self._adres = adres
        self._ploshchad = ploshchad
        self._status = status
        self._data_registracii = data_registracii or datetime.now().isoformat()
        self._data_poslednego_tekh_ucheta = data_poslednego_tekh_ucheta
        self._nomer_tekhpasporta = nomer_tekhpasporta
        self._kadastrovyj_nomer = None
        self._saved_vypiska = saved_vypiska

    @property
    def saved_vypiska(self) -> Optional[str]:
        return self._saved_vypiska

    @saved_vypiska.setter
    def saved_vypiska(self, value: Optional[str]) -> None:
        self._saved_vypiska = value

    @property
    def adres(self) -> str:
        return self._adres

    @adres.setter
    def adres(self, value: str) -> None:
        if not value or not value.strip():
            raise ValidationError("Адрес не может быть пустым")
        self._adres = value

    @property
    def ploshchad(self) -> float:
        return self._ploshchad

    @ploshchad.setter
    def ploshchad(self, value: float) -> None:
        if value <= 0:
            raise ValidationError("Площадь должна быть положительным числом")
        self._ploshchad = value

    @property
    def status(self) -> str:
        return self._status

    @status.setter
    def status(self, value: str) -> None:
        allowed = {"uchtennyy", "vremennyy", "arkhivnyy"}
        if value not in allowed:
            raise ValidationError(f"Статус должен быть одним из {allowed}")
        self._status = value

    @property
    def data_registracii(self) -> str:
        return self._data_registracii

    @property
    def data_poslednego_tekh_ucheta(self) -> Optional[str]:
        return self._data_poslednego_tekh_ucheta

    @data_poslednego_tekh_ucheta.setter
    def data_poslednego_tekh_ucheta(self, value: Optional[str]) -> None:
        self._data_poslednego_tekh_ucheta = value

    @property
    def nomer_tekhpasporta(self) -> Optional[str]:
        return self._nomer_tekhpasporta

    @nomer_tekhpasporta.setter
    def nomer_tekhpasporta(self, value: Optional[str]) -> None:
        self._nomer_tekhpasporta = value

    @property
    def kadastrovyj_nomer(self):
        """Объект КадастровыйНомер, связанный с недвижимостью."""
        return self._kadastrovyj_nomer

    @kadastrovyj_nomer.setter
    def kadastrovyj_nomer(self, value):
        self._kadastrovyj_nomer = value

    def izmenit_status(self, novyj_status: str) -> None:
        """Изменить статус объекта."""
        self.status = novyj_status

