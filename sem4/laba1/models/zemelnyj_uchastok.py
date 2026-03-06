from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from exceptions.exceptions import ValidationError


class zemelnyj_uchastok(objekt_nedvizhimosti):
    """Земельный участок."""

    def __init__(self, kategoriya_zemel: str, vid_razreshonnogo_ispolzovaniya: str,
                 nalichie_postroek: bool = False,
                 sostoyanie: str = "Не указано",
                 **kwargs):
        super().__init__(**kwargs)
        self._kategoriya_zemel = kategoriya_zemel
        self._vid_razreshonnogo_ispolzovaniya = vid_razreshonnogo_ispolzovaniya
        self._nalichie_postroek = nalichie_postroek
        self._sostoyanie = sostoyanie

    @property
    def kategoriya_zemel(self) -> str:
        return self._kategoriya_zemel

    @kategoriya_zemel.setter
    def kategoriya_zemel(self, value: str) -> None:
        if not value:
            raise ValidationError("Категория земель не может быть пустой")
        self._kategoriya_zemel = value

    @property
    def vid_razreshonnogo_ispolzovaniya(self) -> str:
        return self._vid_razreshonnogo_ispolzovaniya

    @vid_razreshonnogo_ispolzovaniya.setter
    def vid_razreshonnogo_ispolzovaniya(self, value: str) -> None:
        if not value:
            raise ValidationError("Вид разрешенного использования не может быть пустым")
        self._vid_razreshonnogo_ispolzovaniya = value

    @property
    def nalichie_postroek(self) -> bool:
        return self._nalichie_postroek

    @nalichie_postroek.setter
    def nalichie_postroek(self, value: bool) -> None:
        self._nalichie_postroek = value

    @property
    def sostoyanie(self) -> str:
        return self._sostoyanie

    @sostoyanie.setter
    def sostoyanie(self, value: str) -> None:
        allowed = ["Отличное", "Хорошее", "Удовлетворительное", "Неудовлетворительное", "Не указано"]
        if value not in allowed:
            raise ValidationError(f"Состояние должно быть одним из {allowed}")
        self._sostoyanie = value