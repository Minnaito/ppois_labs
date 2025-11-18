import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.english_russian_dict import english_russian_dict


def main():
    print("Демонстрация работы Англо-Русского словаря")
    print("=" * 60)

    dictionary = english_russian_dict()

    print("1. Добавление слов в словарь:")
    test_words = [
        ("hello", "привет"),
        ("book", "книга"),
        ("house", "дом"),
        ("cat", "кот"),
        ("dog", "собака"),
        ("apple", "яблоко"),
        ("water", "вода"),
        ("sun", "солнце"),
        ("tree", "дерево"),
        ("car", "машина"),
        ("school", "школа"),
        ("friend", "друг"),
        ("time", "время"),
        ("moon", "луна"),
        ("computer", "компьютер")
    ]

    for english, russian in test_words:
        result = dictionary.add_word(english, russian)
        print(f"   Добавлено: {english} -> {russian} ({'успешно' if result else 'ошибка'})")

    print(f"   Всего слов в словаре: {len(dictionary)}")
    print()

    print("2. Поиск переводов:")
    search_words = ["hello", "book", "unknown", "moon", "school"]
    for word in search_words:
        translation = dictionary.search_translation(word)
        if translation:
            print(f"   '{word}' -> '{translation}'")
        else:
            print(f"   '{word}' -> не найдено")
    print()

    print("3. Использование операторов:")

    dictionary += ("program", "программа")
    print(f"   Добавлено через +=: program -> {dictionary['program']}")
    print(f"   Поиск через []: car -> {dictionary['car']}")
    print(f"   Проверка через in: 'apple' в словаре -> {'apple' in dictionary}")
    print(f"   Проверка через in: 'unknown' в словаре -> {'unknown' in dictionary}")
    print()

    print("4. Демонстрация удаления слов:")
    print(f"   До удаления: {len(dictionary)} слов")
    dictionary -= "dog"
    print(f"   Удалено через -=: dog")
    print(f"   После удаления: {len(dictionary)} слов")

    dictionary.add_word("dog", "собака")
    print(f"   Восстановлено: dog -> собака")
    print(f"   Финальное количество слов: {len(dictionary)}")
    print()

    print("5. Все слова в словаре (отсортированные):")
    all_words = dictionary.display_all_words()
    for i, (eng, rus) in enumerate(all_words, 1):
        print(f"   {i:2d}. {eng:<15} -> {rus}")
    print()

    print("6. Работа с файлами:")

    save_result = dictionary.save_to_file("data/my_dictionary.txt")
    print(f"   Сохранение в файл: {'успешно' if save_result else 'ошибка'}")

    new_dict = english_russian_dict()
    load_result = new_dict.load_from_file("data/my_dictionary.txt")
    print(f"   Загрузка из файла: {'успешно' if load_result else 'ошибка'}")
    print(f"   Загружено слов: {len(new_dict)}")
    print()

    print("7. Работа с C-style строками:")
    import ctypes

    c_english = ctypes.c_char_p(b"language")
    c_russian = ctypes.c_char_p("язык".encode('utf-8'))

    result = dictionary.add_word(c_english, c_russian)
    print(f"   Добавление C-style строк: {'успешно' if result else 'ошибка'}")

    translation = dictionary.search_translation(c_english)
    print(f"   Поиск C-style строк: language -> {translation}")
    print()

    print("8. Валидация данных:")
    invalid_cases = [
        ("", "привет"),
        ("hello", ""),
        ("test123", "тест"),
        ("hello!", "привет"),
        ("a" * 100, "оченьдлинноеслово")
    ]

    for eng, rus in invalid_cases:
        result = dictionary.add_word(eng, rus)
        print(f"   Валидация '{eng}' -> '{rus}': {'принято' if result else 'отклонено'}")
    print()

    print("9. Служебные методы:")
    print(f"   Количество слов: {dictionary.get_word_count()}")
    print(f"   Словарь пуст: {dictionary.is_empty()}")
    print(f"   Булево представление: {bool(dictionary)}")

    dict_str = str(dictionary)
    if len(dict_str) > 50:
        print(f"   Строковое представление: {dict_str[:50]}...")
    else:
        print(f"   Строковое представление: {dict_str}")

    print(f"   Repr представление: {repr(dictionary)}")


if __name__ == "__main__":
    main()
