import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
from src.EnglishRussianDict import EnglishRussianDict


def displayMenu():
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


def addWordInteractive(dictionary):
    print("\n--- Добавление слова ---")
    english = input("Введите английское слово: ").strip().lower()
    if not english:
        print("Ошибка: английское слово не может быть пустым")
        return
    russian = input("Введите русский перевод: ").strip().lower()
    if not russian:
        print("Ошибка: русский перевод не может быть пустым")
        return
    if dictionary.addWord(english, russian):
        print(f"Слово '{english}' -> '{russian}' успешно добавлено!")
    else:
        print("Ошибка добавления слова")


def searchWordInteractive(dictionary):
    print("\n--- Поиск перевода ---")
    if dictionary.isEmpty():
        print("Словарь пуст. Добавьте слова для поиска.")
        return
    word = input("Введите слово для поиска: ").strip().lower()
    translation = dictionary.searchTranslation(word)
    if translation:
        print(f"Перевод: '{word}' -> '{translation}'")
    else:
        print(f"Слово '{word}' не найдено в словаре")


def deleteWordInteractive(dictionary):
    print("\n--- Удаление слова ---")
    if dictionary.isEmpty():
        print("Словарь пуст")
        return
    word = input("Введите слово для удаления: ").strip().lower()
    if word in dictionary:
        dictionary -= word
        print(f"Слово '{word}' успешно удалено!")
    else:
        print(f"Слово '{word}' не найдено в словаре")


def replaceTranslationInteractive(dictionary):
    print("\n--- Замена перевода ---")
    if dictionary.isEmpty():
        print("Словарь пуст. Нечего заменять.")
        return
    word = input("Введите английское слово для замены перевода: ").strip().lower()
    if word not in dictionary:
        print(f"✗ Слово '{word}' не найдено в словаре")
        return
    oldTranslation = dictionary[word]
    print(f"   Текущий перевод: {oldTranslation}")
    newTranslation = input("Введите новый русский перевод: ").strip().lower()
    if not newTranslation:
        print("Ошибка: новый перевод не может быть пустым")
        return
    dictionary[word] = newTranslation
    print(f"Перевод слова '{word}' успешно изменен: '{oldTranslation}' -> '{newTranslation}'")


def showAllWords(dictionary):
    print("\n--- Все слова в словаре ---")
    allWords = dictionary.displayAllWords()
    if allWords:
        print(f"Всего слов: {len(dictionary)}")
        print("-" * 30)
        for i, (eng, rus) in enumerate(allWords, 1):
            print(f"{i:3d}. {eng:<15} -> {rus}")
    else:
        print("Словарь пуст. Добавьте слова для просмотра.")


def saveDictionaryInteractive(dictionary):
    print("\n--- Сохранение словаря ---")
    if dictionary.isEmpty():
        print("Словарь пуст")
        return
    filename = input("Введите имя файла (по умолчанию: data/myDictionary.txt): ").strip()
    if not filename:
        filename = "data/myDictionary.txt"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    if dictionary.saveToFile(filename):
        print(f"Словарь успешно сохранен в файл '{filename}'")
        print(f"Сохранено слов: {len(dictionary)}")
    else:
        print(f"Ошибка сохранения в файл '{filename}'")


def loadDictionaryInteractive(dictionary):
    print("\n--- Загрузка словаря ---")
    filename = input("Введите имя файла (по умолчанию: data/myDictionary.txt): ").strip()
    if not filename:
        filename = "data/myDictionary.txt"
    if not os.path.exists(filename):
        print(f"Файл '{filename}' не существует")
        return
    currentCount = len(dictionary)
    if dictionary.loadFromFile(filename):
        loadedCount = len(dictionary) - currentCount
        print(f"Словарь успешно загружен из файла '{filename}'")
        print(f"Загружено слов: {loadedCount}")
        print(f"Всего слов в словаре: {len(dictionary)}")
    else:
        print(f"Ошибка загрузки из файла '{filename}'")


def demoDictionary(dictionary):
    print("\n" + "=" * 50)
    print("Демонстрация работы словаря")
    print("=" * 50)

    demoDict = EnglishRussianDict()

    print("1. Добавление слов в пустой словарь:")
    testWords = [
        ("hello", "привет"), ("book", "книга"), ("house", "дом"),
        ("cat", "кот"), ("dog", "собака"), ("apple", "яблоко")
    ]
    for eng, rus in testWords:
        demoDict.addWord(eng, rus)
        print(f"   {eng} -> {rus}")
    print(f"\n   Всего слов: {len(demoDict)}")

    print("\n2. Оператор += - добавление нового английского слова и перевода:")
    print("   Добавление через += со строками Python:")
    demoDict += ("program", "программа")
    print(f"   program -> {demoDict['program']}")
    print("\n   Добавление через += с C-style строками:")
    import ctypes
    cEnglish = ctypes.c_char_p(b"computer")
    cRussian = ctypes.c_char_p("компьютер".encode('utf-8'))
    demoDict += (cEnglish, cRussian)
    print(f"   computer -> {demoDict['computer']}")
    print(f"\n   Всего слов после добавления: {len(demoDict)}")

    print("\n3. Оператор -= - удаление существующего английского слова:")
    countBefore = len(demoDict)
    print(f"   До удаления: {countBefore} слов")
    if "book" in demoDict:
        demoDict -= "book"
        countAfter = len(demoDict)
        print(f"   Удалено: book")
        print(f"   После удаления: {countAfter} слов")
        print(f"   Удалено слов: {countBefore - countAfter}")
    else:
        print(f"   Слово 'book' не найдено")

    print("\n4. Оператор [] - поиск перевода английского слова:")
    print(f"   hello -> {demoDict['hello']}")
    print(f"   house -> {demoDict['house']}")
    print(f"   computer -> {demoDict['computer']}")

    print("\n5. Оператор [] - замена перевода английского слова:")
    print(f"   Старый перевод 'hello': {demoDict['hello']}")
    demoDict['hello'] = "здравствуйте"
    print(f"   Новый перевод 'hello': {demoDict['hello']}")

    print("\n6. Определение количества слов в словаре:")
    print(f"   Количество слов в словаре: {len(demoDict)}")

    print("\n7. Возможность загрузки словаря из файла:")
    os.makedirs("data", exist_ok=True)
    demoDict.saveToFile("data/DemoDictionary.txt")
    newDict = EnglishRussianDict()
    newDict.loadFromFile("data/DemoDictionary.txt")
    print(f"   Загружено слов из файла: {len(newDict)}")
    print(f"   Проверка загрузки: 'hello' -> {newDict['hello']}")
    print(f"   Проверка загрузки: 'computer' -> {newDict['computer']}")

    print("\n8. Все слова в словаре:")
    allWords = demoDict.displayAllWords()
    for eng, rus in allWords:
        print(f"   {eng:<12} -> {rus}")


def exitProgram():
    sys.exit(0)


def main():
    dictionary = EnglishRussianDict()
    print("Словарь инициализирован как пустой")

    while True:
        displayMenu()
        choice = input("Выберите действие (0-8): ").strip()
        menuActions = {
            '1': lambda: addWordInteractive(dictionary),
            '2': lambda: searchWordInteractive(dictionary),
            '3': lambda: deleteWordInteractive(dictionary),
            '4': lambda: replaceTranslationInteractive(dictionary),
            '5': lambda: showAllWords(dictionary),
            '6': lambda: saveDictionaryInteractive(dictionary),
            '7': lambda: loadDictionaryInteractive(dictionary),
            '8': lambda: demoDictionary(dictionary),
            '0': lambda: exitProgram()
        }
        if choice in menuActions:
            try:
                menuActions[choice]()
            except Exception as e:
                print(f"Произошла ошибка: {e}")
        else:
            print("Неверный выбор! Пожалуйста, выберите действие от 0 до 8.")


if __name__ == "__main__":
    main()
