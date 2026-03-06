from datetime import datetime
from typing import Optional
from models.base_model import base_model
from exceptions.exceptions import ValidationError

from constants import Constants

class kadastrovyj_nomer(base_model):
    """Кадастровый номер."""

    def __init__(self, nomer_kvartala: str, unikalnyj_nomer_v_kvartale: str,
                 status_nomera: str = Constants.DEFAULT_STATUS,
                 data_prisvoeniya: Optional[str] = None, vladeshec_nomera: Optional['ObjektNedvizhimosti'] = None,
                 **kwargs):
        super().__init__(**kwargs)
        self._nomer_kvartala = nomer_kvartala
        self._unikalnyj_nomer_v_kvartale = unikalnyj_nomer_v_kvartale
        self._status_nomera = status_nomera
        self._data_prisvoeniya = data_prisvoeniya or datetime.now().isoformat()
        self._vladeshec_nomera = vladeshec_nomera

    @property
    def polnoe_znachenie(self) -> str:
        """Полное значение в формате АА:ББ:CCCCCC:DD."""
        return Constants.CADASTRAL_NUMBER_TEMPLATE.format(
            region=Constants.REGION,
            rayon=Constants.RAYON,
            kvartal=self._nomer_kvartala,
            unikalny=self._unikalnyj_nomer_v_kvartale
        )

    @property
    def nomer_kvartala(self) -> str:
        return self._nomer_kvartala

    @property
    def unikalnyj_nomer_v_kvartale(self) -> str:
        return self._unikalnyj_nomer_v_kvartale

    @property
    def status_nomera(self) -> str:
        return self._status_nomera

    @status_nomera.setter
    def status_nomera(self, value: str) -> None:
        if value not in Constants.ALLOWED_STATUSES:
            raise ValidationError(f"Статус номера должен быть одним из {Constants.ALLOWED_STATUSES}")
        self._status_nomera = value

    @property
    def data_prisvoeniya(self) -> str:
        return self._data_prisvoeniya

    @property
    def vladeshec_nomera(self):
        return self._vladeshec_nomera

    @vladeshec_nomera.setter
    def vladeshec_nomera(self, value):
        self._vladeshec_nomera = value

    def proverit_v_reestre(self, other_numbers) -> bool:
        """Проверить уникальность номера среди других."""
        return not any(n.polnoe_znachenie == self.polnoe_znachenie for n in other_numbers)