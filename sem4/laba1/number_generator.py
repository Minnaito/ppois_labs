from models.kadastrovyj_nomer import kadastrovyj_nomer
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from services.cadastral_number_repository import cadastral_number_repository
from exceptions.exceptions import DuplicateError
from constants import Constants

class number_generator:
    """Сервис генерации кадастровых номеров."""

    def __init__(self, repo: cadastral_number_repository):
        self._repo = repo
        self._used_numbers = set(n.polnoe_znachenie for n in repo.list_all())

    def sgenerirovat_nomer(self, objekt: objekt_nedvizhimosti) -> kadastrovyj_nomer:
        """
        Сгенерировать новый кадастровый номер для объекта.
        Упрощённый алгоритм: берём фиксированный квартал и увеличиваем счётчик.
        """
        nomer_kvartala = "000123"
        existing_in_kvartal = [
            n for n in self._repo.list_all()
            if n.nomer_kvartala == nomer_kvartala
        ]
        if existing_in_kvartal:
            max_num = max(int(n.unikalnyj_nomer_v_kvartale) for n in existing_in_kvartal)
            next_num = max_num + Constants.DEFAULT_MIN_POSITIVE
        else:
            next_num = Constants.DEFAULT_MIN_POSITIVE
        unikalnyj_nomer = f"{next_num:03d}"

        number = kadastrovyj_nomer(
            nomer_kvartala=nomer_kvartala,
            unikalnyj_nomer_v_kvartale=unikalnyj_nomer,
            status_nomera="aktivnyy",
            vladeshec_nomera=objekt
        )
        if not number.proverit_v_reestre(self._repo.list_all()):
            raise DuplicateError(f"Номер {number.polnoe_znachenie} уже существует")
        return number

    def zarezervirovat_nomer(self) -> kadastrovyj_nomer:
        """Зарезервировать номер без привязки к объекту."""
        nomer_kvartala = "000123"
        existing = [n for n in self._repo.list_all() if n.nomer_kvartala == nomer_kvartala]
        if existing:
            max_num = max(int(n.unikalnyj_nomer_v_kvartale) for n in existing)
            next_num = max_num + Constants.DEFAULT_MIN_POSITIVE
        else:
            next_num = Constants.DEFAULT_MIN_POSITIVE
        unikalnyj_nomer = f"{next_num:03d}"
        number = kadastrovyj_nomer(
            nomer_kvartala=nomer_kvartala,
            unikalnyj_nomer_v_kvartale=unikalnyj_nomer,
            status_nomera="zarezervirovannyy",
            vladeshec_nomera=None
        )
        return number