from typing import List
from services.owner_repository import owner_repository
from services.object_repository import object_repository
from services.right_document_repository import right_document_repository
from services.cadastral_number_repository import cadastral_number_repository
from services.kadastrovyj_uchet import kadastrovyj_uchet
from services.number_generator import number_generator
from services.tekhnicheskiy_uchet import tekhnicheskiy_uchet
from services.dokument_menedzher import dokument_menedzher
from models.vladeshec import vladeshec
from models.pravo_ustanavlivayushchij_dokument import pravo_ustanavlivayushchij_dokument
from models.zemelnyj_uchastok import zemelnyj_uchastok
from models.zdanie import zdanie
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from exceptions.exceptions import NotFoundError, ValidationError
from datetime import datetime
import uuid


class kadastrovoe_agentstvo:
    """Фасад - основной контроллер системы."""

    def __init__(self, nazvanie: str, data_dir: str = "./data"):
        self.nazvanie = nazvanie
        self._data_dir = data_dir
        self._object_repo = object_repository(data_dir)
        self._owner_repo = owner_repository(data_dir)
        self._right_repo = right_document_repository(data_dir)
        self._cad_number_repo = cadastral_number_repository(data_dir)

        self._restore_relations()

        self._number_generator = number_generator(self._cad_number_repo)
        self._cadastral_service = kadastrovyj_uchet(
        self._object_repo, self._owner_repo, self._right_repo,
        self._cad_number_repo, self._number_generator
        )
        self._technical_service = tekhnicheskiy_uchet(self._object_repo)
        self._document_service = dokument_menedzher(self._object_repo, self._right_repo)

    def _restore_relations(self):
        """Восстановить связи между объектами после загрузки из JSON."""
        objects_by_uid = {obj.uid: obj for obj in self._object_repo.list_all()}
        owners_by_uid = {owner.uid: owner for owner in self._owner_repo.list_all()}
        cad_numbers_by_uid = {cn.uid: cn for cn in self._cad_number_repo.list_all()}

        for doc in self._right_repo.list_all():
            obj_uid = doc.svyazannyj_objekt_uid
            if obj_uid and obj_uid in objects_by_uid:
                doc._svyazannyj_objekt = objects_by_uid[obj_uid]

            doc._spisok_vladelcev = []
            for owner_uid in doc.spisok_vladelcev_uids:
                if owner_uid in owners_by_uid:
                    doc._spisok_vladelcev.append(owners_by_uid[owner_uid])

        for obj in objects_by_uid.values():
            if hasattr(obj, '_kadastrovyj_nomer') and isinstance(obj._kadastrovyj_nomer, str):
                cn_uid = obj._kadastrovyj_nomer
                if cn_uid in cad_numbers_by_uid:
                    cad_number = cad_numbers_by_uid[cn_uid]
                    obj._kadastrovyj_nomer = cad_number
                    cad_number._vladeshec_nomera = obj
                else:
                    obj._kadastrovyj_nomer = None

        for cn in cad_numbers_by_uid.values():
            if hasattr(cn, '_vladeshec_nomera') and isinstance(cn._vladeshec_nomera, str):
                obj_uid = cn._vladeshec_nomera
                if obj_uid in objects_by_uid:
                    cn._vladeshec_nomera = objects_by_uid[obj_uid]

    def sozdat_vladelca(self, identificator: str, fio: str, rekvizity_svyazi: str) -> vladeshec:
        """Создать нового владельца и сохранить в реестре."""
        owner = vladeshec(identificator, fio, rekvizity_svyazi)
        self._owner_repo.add(owner)
        return owner

    def sozdat_zemelnyj_uchastok(self, adres: str, ploshchad: float,
                                 kategoriya_zemel: str, vid_ispolzovaniya: str) -> zemelnyj_uchastok:
        """Создать земельный участок."""
        obj = zemelnyj_uchastok(
            adres=adres,
            ploshchad=ploshchad,
            kategoriya_zemel=kategoriya_zemel,
            vid_razreshonnogo_ispolzovaniya=vid_ispolzovaniya
        )
        self._object_repo.add(obj)
        return obj

    def sozdat_zdanie(self, adres: str, ploshchad: float,
                      etazhi: int, material: str, naznachenie: str, god: int) -> zdanie:
        """Создать здание."""
        obj = zdanie(
            adres=adres,
            ploshchad=ploshchad,
            kolichestvo_etazhej=etazhi,
            material_sten=material,
            naznachenie=naznachenie,
            god_postrojki=god
        )
        self._object_repo.add(obj)
        return obj

    def vypolnit_registraciyu(self, objekt_id: str, owner_id: str,
                              doc_nomer: str, doc_data: str, doc_organ: str,
                              tip_prava: str, dolya: float) -> pravo_ustanavlivayushchij_dokument:
        obj = self._object_repo.get(objekt_id)
        owner = self._owner_repo.get(owner_id)

        existing_docs = [doc for doc in self._right_repo.list_all() if doc.svyazannyj_objekt == obj]
        current_sum = sum(doc.dolya_v_prave for doc in existing_docs)
        if current_sum + dolya > 1.0 + 1e-9:
            raise ValidationError(
                f"Сумма долей по объекту не может превышать 1. "
                f"Текущая сумма: {current_sum}, добавляемая доля: {dolya}"
            )

        doc = pravo_ustanavlivayushchij_dokument(
            nomer_dokumenta=doc_nomer,
            data_vydachi=doc_data,
            organ_vydachi=doc_organ,
            tip_prava=tip_prava,
            dolya_v_prave=dolya,
            svyazannyj_objekt=obj,
            spisok_vladelcev=[owner]
        )

        self._cadastral_service.postavit_na_uchet(obj, owner, doc)
        return doc

    def vydat_kadastrovyj_nomer(self, objekt_id: str):
        """Выдать кадастровый номер для объекта (если ещё не присвоен)."""
        obj = self._object_repo.get(objekt_id)
        if obj.kadastrovyj_nomer:
            print(f"Объекту уже присвоен номер {obj.kadastrovyj_nomer.polnoe_znachenie}")
            return obj.kadastrovyj_nomer
        cad_number = self._number_generator.sgenerirovat_nomer(obj)
        obj.kadastrovyj_nomer = cad_number
        cad_number.vladeshec_nomera = obj
        self._cad_number_repo.add(cad_number)
        self._object_repo.update(obj)
        return cad_number

    def provesti_tekhnicheskij_uchet(self, objekt_id: str, **parametry):
        """Провести технический учёт с формированием техпаспорта."""
        obj = self._object_repo.get(objekt_id)

        if isinstance(obj, zdanie):
            self._technical_service.provesti_tekhnicheskij_uchet_zdaniya(obj, parametry)
        elif isinstance(obj, zemelnyj_uchastok):
            self._technical_service.provesti_tekhnicheskij_uchet_uchastka(obj, parametry)
        else:
            for key, value in parametry.items():
                if hasattr(obj, key):
                    setattr(obj, key, value)
            obj.data_poslednego_tekh_ucheta = datetime.now().isoformat()
            obj.nomer_tekhpasporta = f"ТП-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}"
            self._object_repo.update(obj)
        return obj

    def obnovit_dokumenty(self, objekt_id: str) -> str:
        """Обновить документацию по объекту (сгенерировать и сохранить выписку)."""
        obj = self._object_repo.get(objekt_id)
        return self._document_service.obnovit_dokumentatsiyu(obj)

    def predostavit_informaciyu(self, kadastrovyj_nomer_str: str) -> str:
        """Предоставить сохранённую выписку по кадастровому номеру."""
        for obj in self._object_repo.list_all():
            if obj.kadastrovyj_nomer and obj.kadastrovyj_nomer.polnoe_znachenie == kadastrovyj_nomer_str:
                saved = self._document_service.get_saved_vypiska(obj)
                if saved is not None:
                    return saved
                else:
                    return f"Документация для объекта {kadastrovyj_nomer_str} не оформлена. Выполните пункт 7 меню."
        raise NotFoundError(f"Объект с кадастровым номером {kadastrovyj_nomer_str} не найден")

    @property
    def reestr_obektov(self) -> List[objekt_nedvizhimosti]:
        objects = self._object_repo.list_all()
        print(f"reestr_obektov вызван, найдено объектов: {len(objects)}")
        return objects

    @property
    def reestr_vladelcev(self) -> List[vladeshec]:
        return self._owner_repo.list_all()