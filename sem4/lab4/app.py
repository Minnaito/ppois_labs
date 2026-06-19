import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, render_template, request, redirect, url_for, flash
from services.kadastrovoe_agentstvo import kadastrovoe_agentstvo
from exceptions.exceptions import NotFoundError, ValidationError
from models.zdanie import zdanie
from models.zemelnyj_uchastok import zemelnyj_uchastok
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'cadastre-secret-key-2026'

agency = kadastrovoe_agentstvo("Городское кадастровое агентство", data_dir="./data")

ORGANS = ['Суд', 'Нотариус', 'Росреестр', 'Орган местного самоуправления']
RIGHT_TYPES = ['sobstvennost', 'arenda', 'nasledstvo']
RIGHT_TYPES_RU = {'sobstvennost': 'Собственность', 'arenda': 'Аренда', 'nasledstvo': 'Наследство'}
LAND_CATEGORIES = ['Сельскохозяйственное назначение', 'Населённые пункты',
                   'Промышленное назначение', 'Особо охраняемые территории']
PERMITTED_USES = ['ИЖС', 'ЛПХ', 'Садоводство', 'Коммерческая']
BUILDING_PURPOSES = ['zhiloe', 'nezhiloe']
BUILDING_PURPOSES_RU = {'zhiloe': 'Жилое', 'nezhiloe': 'Нежилое'}
LAND_STATES = ['Отличное', 'Хорошее', 'Удовлетворительное', 'Неудовлетворительное', 'Не указано']


def format_date(date_str):
    if not date_str:
        return "не указана"
    try:
        if 'T' in date_str:
            dt = datetime.fromisoformat(date_str)
            return dt.strftime('%d.%m.%Y')
        return date_str
    except:
        return date_str


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/owners')
def list_owners():
    owners = agency.reestr_vladelcev
    return render_template('owners.html', owners=owners)


@app.route('/owner/create', methods=['GET', 'POST'])
def create_owner():
    if request.method == 'POST':
        try:
            identificator = request.form['identificator']
            fio = request.form['fio']
            rekvizity = request.form['rekvizity']
            owner = agency.sozdat_vladelca(identificator, fio, rekvizity)
            flash(f'Владелец "{owner.fio}" успешно создан!', 'success')
            return redirect(url_for('list_owners'))
        except ValidationError as e:
            flash(f'Ошибка: {e}', 'danger')
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
    return render_template('create_owner.html')


@app.route('/objects')
def list_objects():
    objects = agency.reestr_obektov
    obj_list = []
    for obj in objects:
        if isinstance(obj, zemelnyj_uchastok):
            obj_type = 'ZemelnyjUchastok'
            type_ru = 'Земельный участок'
        elif isinstance(obj, zdanie):
            obj_type = 'Zdanie'
            type_ru = 'Здание'
        else:
            obj_type = obj.__class__.__name__
            type_ru = 'Объект'

        obj_list.append({
            'obj': obj,
            'type': obj_type,
            'type_ru': type_ru
        })
    return render_template('objects.html', objects=obj_list)


@app.route('/object/create/land', methods=['GET', 'POST'])
def create_land():
    if request.method == 'POST':
        try:
            adres = request.form['adres']
            ploshchad = float(request.form['ploshchad'])
            kategoriya = request.form['kategoriya']
            vid = request.form['vid']
            obj = agency.sozdat_zemelnyj_uchastok(adres, ploshchad, kategoriya, vid)
            flash(f'Земельный участок по адресу "{obj.adres}" создан!', 'success')
            return redirect(url_for('list_objects'))
        except ValidationError as e:
            flash(f'Ошибка: {e}', 'danger')
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
    return render_template('create_land.html',
                           land_categories=LAND_CATEGORIES,
                           permitted_uses=PERMITTED_USES)


@app.route('/object/create/building', methods=['GET', 'POST'])
def create_building():
    if request.method == 'POST':
        try:
            adres = request.form['adres']
            ploshchad = float(request.form['ploshchad'])
            etazhi = int(request.form['etazhi'])
            material = request.form['material']
            naznachenie = request.form['naznachenie']
            god = int(request.form['god'])
            obj = agency.sozdat_zdanie(adres, ploshchad, etazhi, material, naznachenie, god)
            flash(f'Здание по адресу "{obj.adres}" создано!', 'success')
            return redirect(url_for('list_objects'))
        except ValidationError as e:
            flash(f'Ошибка: {e}', 'danger')
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')
    return render_template('create_building.html',
                           building_purposes=BUILDING_PURPOSES,
                           building_purposes_ru=BUILDING_PURPOSES_RU)


@app.route('/rights')
def rights():
    rights_list = agency._right_repo.list_all()
    owners = agency.reestr_vladelcev
    objects = agency.reestr_obektov
    return render_template('rights.html', rights=rights_list, owners=owners, objects=objects)


@app.route('/right/register', methods=['POST'])
def register_right():
    try:
        objekt_id = request.form['objekt_id']
        owner_id = request.form['owner_id']
        doc_nomer = request.form['doc_nomer']
        doc_data = request.form['doc_data']
        doc_organ = request.form['doc_organ']
        tip_prava = request.form['tip_prava']
        dolya = float(request.form['dolya'])

        doc = agency.vypolnit_registraciyu(
            objekt_id, owner_id, doc_nomer, doc_data, doc_organ, tip_prava, dolya
        )
        flash(f'Право зарегистрировано! Документ: {doc.nomer_dokumenta}', 'success')
        return redirect(url_for('rights'))
    except ValidationError as e:
        flash(f'Ошибка: {e}', 'danger')
    except NotFoundError as e:
        flash(f'Ошибка: {e}', 'danger')
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('rights'))


@app.route('/cadastral/assign/<object_id>', methods=['POST'])
def assign_cadastral_number(object_id):
    try:
        cad_number = agency.vydat_kadastrovyj_nomer(object_id)
        flash(f'Кадастровый номер присвоен: {cad_number.polnoe_znachenie}', 'success')
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('list_objects'))


@app.route('/technical/accounting/<object_id>', methods=['GET', 'POST'])
def technical_accounting(object_id):
    try:
        obj = agency._object_repo.get(object_id)
    except NotFoundError:
        flash('Объект не найден', 'danger')
        return redirect(url_for('list_objects'))

    if request.method == 'POST':
        try:
            params = {}
            if request.form.get('adres'):
                params['adres'] = request.form['adres']
            if request.form.get('ploshchad'):
                params['ploshchad'] = float(request.form['ploshchad'])

            if isinstance(obj, zdanie):
                if request.form.get('kolichestvo_etazhej'):
                    params['kolichestvo_etazhej'] = int(request.form['kolichestvo_etazhej'])
                if request.form.get('material_sten'):
                    params['material_sten'] = request.form['material_sten']
                if request.form.get('naznachenie'):
                    params['naznachenie'] = request.form['naznachenie']
                if request.form.get('god_postrojki'):
                    params['god_postrojki'] = int(request.form['god_postrojki'])
            else:
                if request.form.get('kategoriya_zemel'):
                    params['kategoriya_zemel'] = request.form['kategoriya_zemel']
                if request.form.get('vid_razreshonnogo_ispolzovaniya'):
                    params['vid_razreshonnogo_ispolzovaniya'] = request.form['vid_razreshonnogo_ispolzovaniya']
                params['nalichie_postroek'] = 'nalichie_postroek' in request.form
                if request.form.get('sostoyanie'):
                    params['sostoyanie'] = request.form['sostoyanie']

            updated_obj = agency.provesti_tekhnicheskij_uchet(object_id, **params)
            flash(f'Технический учёт проведён! Техпаспорт №{updated_obj.nomer_tekhpasporta}', 'success')
            return redirect(url_for('list_objects'))
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')

    return render_template('technical_accounting.html', obj=obj, land_states=LAND_STATES)


@app.route('/document/update/<object_id>', methods=['POST'])
def update_documentation(object_id):
    try:
        agency.obnovit_dokumenty(object_id)
        flash('Документация обновлена', 'success')
    except Exception as e:
        flash(f'Ошибка: {e}', 'danger')
    return redirect(url_for('list_objects'))


@app.route('/extract', methods=['GET', 'POST'])
def get_extract():
    extract_text = None
    if request.method == 'POST':
        kad_num = request.form.get('kadastrovyj_nomer')
        try:
            extract_text = agency.predostavit_informaciyu(kad_num)
            flash('Выписка успешно получена', 'success')
        except NotFoundError as e:
            flash(f'Ошибка: {e}', 'danger')
        except Exception as e:
            flash(f'Ошибка: {e}', 'danger')

    objects_with_numbers = [
        obj for obj in agency.reestr_obektov
        if obj.kadastrovyj_nomer is not None
    ]
    return render_template('extract.html',
                           extract_text=extract_text,
                           objects_with_numbers=objects_with_numbers)


@app.route('/extract_text/<cadastral_number>')
def get_extract_text(cadastral_number):
    """API для получения текста выписки (для AJAX)"""
    try:
        extract_text = agency.predostavit_informaciyu(cadastral_number)
        return extract_text
    except NotFoundError as e:
        return str(e), 404
    except Exception as e:
        return str(e), 500


if __name__ == '__main__':
    os.makedirs("./data", exist_ok=True)
    app.run(debug=True, host='0.0.0.0', port=5000)