from models.vladeshec import vladeshec
from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from services.number_generator import number_generator
from services.owner_repository import owner_repository
from services.object_repository import object_repository
from services.right_document_repository import right_document_repository
from services.cadastral_number_repository import cadastral_number_repository


class kadastrovyj_uchet:
    """Сервис кадастрового учёта."""

    def __init__(self,
                 object_repo: object_repository,
                 owner_repo: owner_repository,
                 right_repo: right_document_repository,
                 cad_number_repo: cadastral_number_repository,
                 number_generator: number_generator):
        self._object_repo = object_repo
        self._owner_repo = owner_repo
        self._right_repo = right_repo
        self._cad_number_repo = cad_number_repo
        self._number_generator = number_generator

    def postavit_na_uchet(self, objekt: objekt_nedvizhimosti,
                          vladelec: vladeshec,
                          dokument: pravo_ustanavlivayushchij_dokument) -> None:
        """
        Поставить объект на кадастровый учёт.
        """
        if vladelec not in dokument.spisok_vladelcev:
            dokument.spisok_vladelcev.append(vladelec)


        objekt.izmenit_status("uchtennyy")

        self._object_repo.add(objekt)
        self._owner_repo.add(vladelec)
        self._right_repo.add(dokument)