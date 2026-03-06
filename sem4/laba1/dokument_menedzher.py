from datetime import datetime
from typing import Optional

from models.vladeshec import vladeshec
from models.objekt_nedvizhimosti import objekt_nedvizhimosti
from models.zdanie import zdanie
from models.zemelnyj_uchastok import zemelnyj_uchastok
from services.object_repository import object_repository
from services.right_document_repository import right_document_repository
from exceptions.exceptions import PermissionDeniedError
from constants import Constants


class dokument_menedzher:
    """Сервис документооборота."""

    def __init__(self, object_repo: object_repository, right_repo: right_document_repository):
        self._object_repo = object_repo
        self._right_repo = right_repo

    def obnovit_dokumentatsiyu(self, objekt: objekt_nedvizhimosti) -> str:
        """
        Сгенерировать новую версию выписки и сохранить её в объекте.
        Возвращает текст выписки.
        """
        vypiska = self._generate_vypiska(objekt)
        objekt.saved_vypiska = vypiska
        self._object_repo.update(objekt)
        return vypiska

    def get_saved_vypiska(self, objekt: objekt_nedvizhimosti) -> Optional[str]:
        """Вернуть сохранённую выписку, если она есть."""
        return objekt.saved_vypiska

    def zaprosit_vypisku(self, objekt: objekt_nedvizhimosti, zayavitel: vladeshec) -> str:
        """
        Запросить выписку по объекту с проверкой прав заявителя.
        """
        if not self._check_access(objekt, zayavitel):
            raise PermissionDeniedError("Заявитель не имеет прав на получение выписки по этому объекту")
        return self._generate_vypiska(objekt)

    def _check_access(self, objekt: objekt_nedvizhimosti, zayavitel: vladeshec) -> bool:
        """Проверка прав доступа."""
        for doc in self._right_repo.list_all():
            if doc.svyazannyj_objekt == objekt and zayavitel in doc.spisok_vladelcev:
                return True
        return False

    def _format_date(self, date_str: Optional[str]) -> str:
        """Форматирование даты из ISO в ДД.ММ.ГГГГ."""
        if not date_str:
            return "не указана"
        try:
            if 'T' in date_str:
                dt = datetime.fromisoformat(date_str)
                return dt.strftime('%d.%m.%Y')
            for fmt in ['%Y-%m-%d', '%d.%m.%Y']:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return dt.strftime('%d.%m.%Y')
                except ValueError:
                    continue
            return date_str
        except:
            return date_str

    def _get_iznos_level(self, iznos: int) -> str:
        """Возвращает текстовую градацию износа."""
        if iznos < Constants.DEPRECIATION_EXCELLENT:
            return "Отличное"
        elif iznos < Constants.DEPRECIATION_GOOD:
            return "Хорошее"
        elif iznos < Constants.DEPRECIATION_SATISFACTORY:
            return "Удовлетворительное"
        elif iznos < Constants.DEPRECIATION_POOR:
            return "Неудовлетворительное"
        else:
            return "Аварийное"

    def _generate_vypiska(self, objekt: objekt_nedvizhimosti) -> str:
        """Сгенерировать текст выписки."""

        object_types = {
            'ZemelnyjUchastok': 'Земельный участок',
            'Zdanie': 'Здание',
            'ObjektNedvizhimosti': 'Объект недвижимости'
        }
        object_type = object_types.get(objekt.__class__.__name__, objekt.__class__.__name__)

        status_map = {
            'uchtennyy': 'Учтённый',
            'vremennyy': 'Временный',
            'arkhivnyy': 'Архивный'
        }
        status = status_map.get(objekt.status, objekt.status)

        data_reg = self._format_date(objekt.data_registracii)

        lines = [
            f"ВЫПИСКА ИЗ ЕДИНОГО ГОСУДАРСТВЕННОГО РЕЕСТРА НЕДВИЖИМОСТИ",
            f"Объект: {object_type}",
            f"Адрес: {objekt.adres}",
            f"Площадь: {objekt.ploshchad} кв.м",
            f"Статус: {status}",
            f"Дата регистрации: {data_reg}",
        ]

        if objekt.kadastrovyj_nomer:
            lines.append(f"Кадастровый номер: {objekt.kadastrovyj_nomer.polnoe_znachenie}")
        else:
            lines.append("Кадастровый номер: не присвоен")

        if objekt.nomer_tekhpasporta:
            data_tekh = self._format_date(objekt.data_poslednego_tekh_ucheta)
            lines.append(f"Технический паспорт: №{objekt.nomer_tekhpasporta} от {data_tekh}")

            if isinstance(objekt, zdanie):
                iznos_level = self._get_iznos_level(objekt.fizicheskij_iznos)
                lines.append(f"   Физический износ: {objekt.fizicheskij_iznos}% ({iznos_level})")
                lines.append(f"   Этажность: {objekt.kolichestvo_etazhej}")
                lines.append(f"   Материал стен: {objekt.material_sten}")
                lines.append(f"   Пожарная безопасность: класс {objekt.pozharnaya_bezopasnost}")
                lines.append(f"   Энергоэффективность: класс {objekt.energeticheskaya_effektivnost}")

            elif isinstance(objekt, zemelnyj_uchastok):
                lines.append(f"   Категория земель: {objekt.kategoriya_zemel}")
                lines.append(f"   Вид использования: {objekt.vid_razreshonnogo_ispolzovaniya}")
                lines.append(f"   Наличие построек: {'Да' if objekt.nalichie_postroek else 'Нет'}")
                lines.append(f"   Состояние участка: {objekt.sostoyanie}")
        else:
            lines.append("Технический паспорт: не оформлен")

        vladeshec = []
        right_type_map = {
            'sobstvennost': 'Собственность',
            'arenda': 'Аренда',
            'nasledstvo': 'Наследство',
            'other': 'Другое'
        }

        for doc in self._right_repo.list_all():
            if doc.svyazannyj_objekt == objekt:
                for vl in doc.spisok_vladelcev:
                    right_type = right_type_map.get(doc.tip_prava, doc.tip_prava)
                    vladeshec.append(f"{vl.fio} ({right_type}, доля {doc.dolya_v_prave})")

        if vladeshec:
            lines.append("Правообладатели: " + "; ".join(vladeshec))
        else:
            lines.append("Правообладатели: не зарегистрированы")

        return "\n".join(lines)