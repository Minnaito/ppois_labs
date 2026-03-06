from typing import List, Optional, TYPE_CHECKING
from models.base_model import base_model
from models.dokument import dokument
from models.vladeshec import vladeshec
from exceptions.exceptions import ValidationError
from constants import Constants

if TYPE_CHECKING:
    from models.objekt_nedvizhimosti import objekt_nedvizhimosti


class pravo_ustanavlivayushchij_dokument(base_model, dokument):
    """Правоустанавливающий документ, связывающий владельцев и объект."""

    def __init__(self,
                 tip_prava: str,
                 dolya_v_prave: float,
                 svyazannyj_objekt: 'objekt_nedvizhimosti',
                 spisok_vladelcev: List[vladeshec],
                 nomer_dokumenta: str = '',
                 data_vydachi: str = '',
                 organ_vydachi: str = '',
                 **kwargs):
        base_model.__init__(self, **kwargs)

        dokument.__init__(
            self,
            nomer_dokumenta=nomer_dokumenta,
            data_vydachi=data_vydachi,
            organ_vydachi=organ_vydachi
        )

        self._tip_prava = tip_prava
        self._dolya_v_prave = dolya_v_prave
        self._svyazannyj_objekt = svyazannyj_objekt
        self._spisok_vladelcev = spisok_vladelcev

        if svyazannyj_objekt:
            self._svyazannyj_objekt_uid = svyazannyj_objekt.uid
        else:
            self._svyazannyj_objekt_uid = None

        self._spisok_vladelcev_uids = [v.uid for v in spisok_vladelcev] if spisok_vladelcev else []

    @property
    def tip_prava(self) -> str:
        return self._tip_prava

    @tip_prava.setter
    def tip_prava(self, value: str) -> None:
        allowed = {"sobstvennost", "arenda", "nasledstvo"}
        if value not in allowed:
            raise ValidationError(f"Тип права должен быть одним из {allowed}")
        self._tip_prava = value

    @property
    def dolya_v_prave(self) -> float:
        return self._dolya_v_prave

    @dolya_v_prave.setter
    def dolya_v_prave(self, value: float) -> None:
        if not (Constants.MIN_DEPRECIATION < value <= Constants.MAX_DEPRECIATION):
            raise ValidationError("Доля в праве должна быть в интервале (0, 1]")
        self._dolya_v_prave = value

    @property
    def svyazannyj_objekt(self):
        return self._svyazannyj_objekt

    @property
    def spisok_vladelcev(self) -> List[vladeshec]:
        return self._spisok_vladelcev

    @property
    def nomer_dokumenta(self) -> str:
        return self._nomer_dokumenta

    @property
    def data_vydachi(self) -> str:
        return self._data_vydachi

    @property
    def organ_vydachi(self) -> str:
        return self._organ_vydachi

    @property
    def svyazannyj_objekt_uid(self) -> Optional[str]:
        return self._svyazannyj_objekt_uid

    @property
    def spisok_vladelcev_uids(self) -> List[str]:
        return self._spisok_vladelcev_uids
