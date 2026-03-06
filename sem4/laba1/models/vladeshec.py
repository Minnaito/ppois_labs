from models.base_model import base_model
from exceptions.exceptions import ValidationError


class vladeshec(base_model):
    """Владелец недвижимости."""

    def __init__(self, identificator: str, fio: str, rekvizity_svyazi: str, **kwargs):
        super().__init__(**kwargs)
        self._identificator = identificator
        self._fio = fio
        self._rekvizity_svyazi = rekvizity_svyazi

    @property
    def identificator(self) -> str:
        """ИНН или паспортные данные."""
        return self._identificator

    @identificator.setter
    def identificator(self, value: str) -> None:
        if not value:
            raise ValidationError("Идентификатор не может быть пустым")
        self._identificator = value

    @property
    def fio(self) -> str:
        return self._fio

    @fio.setter
    def fio(self, value: str) -> None:
        if not value:
            raise ValidationError("ФИО не может быть пустым")
        self._fio = value

    @property
    def rekvizity_svyazi(self) -> str:
        return self._rekvizity_svyazi

    @rekvizity_svyazi.setter
    def rekvizity_svyazi(self, value: str) -> None:
        if not value:
            raise ValidationError("Реквизиты связи не могут быть пустыми")
        self._rekvizity_svyazi = value