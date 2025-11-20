import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.english_russian_dict import english_russian_dict


def display_menu():
    print("\n" + "=" * 60)
    print("          АНГЛО-РУССКИЙ СЛОВАРЬ - ГЛАВНОЕ МЕНЮ")
    print("=" * 60)
    print("1. Добавить слово в словарь")
    print("2. Найти перевод слова")
    print("3. Удалить слово из словаря")
    print("4. Заменить перевод слова")
    print("5. Показать все слова")
    print("6. Сохранить словарь в файл")
    print("7. Загрузить словарь из файла")
    print("8. Демонстрация работы словаря")
    print("0. Выход")
    print("-" * 60)


def add_word_interactive(dictionary):
    print("\n--- Добавление слова ---")
    english = input("Введите английское слово: ").strip().lower()
    if not english:
        print("Ошибка: английское слово не может быть пустым")
        return
    russian = input("Введите русский перевод: ").strip().lower()
    if not russian:
        print("Ошибка: русский перевод не может быть пустым")
        return
    if dictionary.add_word(english, russian):
        print(f"Слово '{english}' -> '{russian}' успешно добавлено!")
    else:
        print("Ошибка добавления слова")


def search_word_interactive(dictionary):
    print("\n--- Поиск перевода ---")
    if dictionary.is_empty():
        print("Словарь пуст. Добавьте слова для поиска.")
        return
    word = input("Введите слово для поиска: ").strip().lower()
    translation = dictionary.search_translation(word)
    if translation:
        print(f"Перевод: '{word}' -> '{translation}'")
    else:
        print(f"Слово '{word}' не найдено в словаре")


def delete_word_interactive(dictionary):
    print("\n--- Удаление слова ---")
    if dictionary.is_empty():
        print("Словарь пуст")
        return
    word = input("Введите слово для удаления: ").strip().lower()
    if word in dictionary:
        dictionary -= word
        print(f"Слово '{word}' успешно удалено!")
    else:
        print(f"Слово '{word}' не найдено в словаре")


def replace_translation_interactive(dictionary):
    print("\n--- Замена перевода ---")
    if dictionary.is_empty():
        print("Словарь пуст. Нечего заменять.")
        return
    word = input("Введите английское слово для замены перевода: ").strip().lower()
    if word not in dictionary:
        print(f"✗ Слово '{word}' не найдено в словаре")
        return
    old_translation = dictionary[word]
    print(f"   Текущий перевод: {old_translation}")
    new_translation = input("Введите новый русский перевод: ").strip().lower()
    if not new_translation:
        print("Ошибка: новый перевод не может быть пустым")
        return
    dictionary[word] = new_translation
    print(f"Перевод слова '{word}' успешно изменен: '{old_translation}' -> '{new_translation}'")


def show_all_words(dictionary):
    print("\n--- Все слова в словаре ---")
    all_words = dictionary.display_all_words()
    if all_words:
        print(f"Всего слов: {len(dictionary)}")
        print("-" * 30)
        for i, (eng, rus) in enumerate(all_words, 1):
            print(f"{i:3d}. {eng:<15} -> {rus}")
    else:
        print("Словарь пуст. Добавьте слова для просмотра.")


def save_dictionary_interactive(dictionary):
    print("\n--- Сохранение словаря ---")
    if dictionary.is_empty():
        print("Словарь пуст")
        return
    filename = input("Введите имя файла (по умолчанию: data/my_dictionary.txt): ").strip()
    if not filename:
        filename = "data/my_dictionary.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if dictionary.save_to_file(filename):
        print(f"Словарь успешно сохранен в файл '{filename}'")
        print(f"Сохранено слов: {len(dictionary)}")
    else:
        print(f"Ошибка сохранения в файл '{filename}'")


def load_dictionary_interactive(dictionary):
    print("\n--- Загрузка словаря ---")
    filename = input("Введите имя файла (по умолчанию: data/my_dictionary.txt): ").strip()
    if not filename:
        filename = "data/my_dictionary.txt"
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не существует")
        return
    current_count = len(dictionary)
    if dictionary.load_from_file(filename):
        loaded_count = len(dictionary) - current_count
        print(f"Словарь успешно загружен из файла '{filename}'")
        print(f"Загружено слов: {loaded_count}")
        print(f"Всего слов в словаре: {len(dictionary)}")
    else:
        print(f"Ошибка загрузки из файла '{filename}'")


def demo_dictionary(dictionary):
    print("\n" + "=" * 50)
    print("Демонстрация работы словаря")
    print("=" * 50)

    demo_dict = english_russian_dict()

    print("1. Добавление слов в пустой словарь:")
    test_words = [
        ("hello", "привет"), ("book", "книга"), ("house", "дом"),
        ("cat", "кот"), ("dog", "собака"), ("apple", "яблоко")
    ]
    for eng, rus in test_words:
        demo_dict.add_word(eng, rus)
        print(f"   {eng} -> {rus}")
    print(f"\n   Всего слов: {len(demo_dict)}")

    print("\n2. Оператор += - добавление нового английского слова и перевода:")
    print("   Добавление через += со строками Python:")
    demo_dict += ("program", "программа")
    print(f"   program -> {demo_dict['program']}")
    print("\n   Добавление через += с C-style строками:")
    import ctypes
    c_english = ctypes.c_char_p(b"computer")
    c_russian = ctypes.c_char_p("компьютер".encode('utf-8'))
    demo_dict += (c_english, c_russian)
    print(f"   computer -> {demo_dict['computer']}")
    print(f"\n   Всего слов после добавления: {len(demo_dict)}")

    print("\n3. Оператор -= - удаление существующего английского слова:")
    count_before = len(demo_dict)
    print(f"   До удаления: {count_before} слов")
    if "book" in demo_dict:
        demo_dict -= "book"
        count_after = len(demo_dict)
        print(f"   Удалено: book")
        print(f"   После удаления: {count_after} слов")
        print(f"   Удалено слов: {count_before - count_after}")
    else:
        print(f"   Слово 'book' не найдено")

    print("\n4. Оператор [] - поиск перевода английского слова:")
    print(f"   hello -> {demo_dict['hello']}")
    print(f"   house -> {demo_dict['house']}")
    print(f"   computer -> {demo_dict['computer']}")

    print("\n5. Оператор [] - замена перевода английского слова:")
    print(f"   Старый перевод 'hello': {demo_dict['hello']}")
    demo_dict['hello'] = "здравствуйте"
    print(f"   Новый перевод 'hello': {demo_dict['hello']}")

    print("\n6. Определение количества слов в словаре:")
    print(f"   Количество слов в словаре: {len(demo_dict)}")

    print("\n7. Возможность загрузки словаря из файла:")
    os.makedirs("data", exist_ok=True)
    demo_dict.save_to_file("data/demo_dictionary.txt")
    new_dict = english_russian_dict()
    new_dict.load_from_file("data/demo_dictionary.txt")
    print(f"   Загружено слов из файла: {len(new_dict)}")
    print(f"   Проверка загрузки: 'hello' -> {new_dict['hello']}")
    print(f"   Проверка загрузки: 'computer' -> {new_dict['computer']}")

    print("\n8. Все слова в словаре:")
    all_words = demo_dict.display_all_words()
    for eng, rus in all_words:
        print(f"   {eng:<12} -> {rus}")


def exit_program():
    sys.exit(0)


def main():
    dictionary = english_russian_dict()
    print("Словарь инициализирован как пустой")

    while True:
        display_menu()
        choice = input("Выберите действие (0-8): ").strip()
        menu_actions = {
            '1': lambda: add_word_interactive(dictionary),
            '2': lambda: search_word_interactive(dictionary),
            '3': lambda: delete_word_interactive(dictionary),
            '4': lambda: replace_translation_interactive(dictionary),
            '5': lambda: show_all_words(dictionary),
            '6': lambda: save_dictionary_interactive(dictionary),
            '7': lambda: load_dictionary_interactive(dictionary),
            '8': lambda: demo_dictionary(dictionary),
            '0': lambda: exit_program()
        }
        if choice in menu_actions:
            try:
                menu_actions[choice]()
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        else:
            print("Неверный выбор! Пожалуйста, выберите действие от 0 до 8.")


if __name__ == "__main__":
    main()
