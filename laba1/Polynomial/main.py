import unittest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.Polynomial import Polynomial


def displayMenu():
    print("\n" + "=" * 50)
    print("          РАБОТА С МНОГОЧЛЕНАМИ")
    print("=" * 50)
    print("1. Создать многочлен")
    print("2. Вычислить значение многочлена (оператор ())")
    print("3. Получить коэффициенты многочлена (оператор [])")
    print("4. Сложение многочленов (оператор +)")
    print("5. Сложение с присваиванием (оператор +=)")
    print("6. Вычитание многочленов (оператор -)")
    print("7. Вычитание с присваиванием (оператор -=)")
    print("8. Умножение многочленов (оператор *)")
    print("9. Умножение с присваиванием (оператор *=)")
    print("10. Деление многочленов (оператор /)")
    print("11. Деление с присваиванием (оператор /=)")
    print("12. Показать все многочлены")
    print("13. Демонстрация работы операторов")
    print("0. Выход")
    print("-" * 50)

def createPolynomialInteractive(polynomialsList):
    print("\n--- Создание многочлена ---")
    print("Примеры ввода:")
    print("  • 2x² - 3x + 1 → введите: 2 -3 1")
    print("  • x³ - 2x + 5 → введите: 1 0 -2 5")
    print("  • 4x + 7 → введите: 4 7")
    print("  • 5 → введите: 5")

    try:
        coefficientsInput = input("\nВведите коэффициенты через пробел (старшая степень первая): ")
        coefficientsList = [float(number) for number in coefficientsInput.split()]

        if not coefficientsList:
            print("Ошибка: не введены коэффициенты")
            return

        newPolynomial = Polynomial(coefficientsList)
        polynomialsList.append(newPolynomial)
        print(f"✓ Создан многочлен: {newPolynomial}")
        print(f"✓ Степень: {newPolynomial.degree}")

    except ValueError:
        print(" Ошибка: введите только числа через пробел")
        print(" Например: '2 -3 1' для многочлена 2x² - 3x + 1")


def evaluatePolynomialInteractive(polynomialsList):
    print("\n--- Вычисление значения многочлена (оператор ()) ---")

    if not polynomialsList:
        print("Сначала создайте многочлены")
        return

    showPolynomials(polynomialsList)

    try:
        polynomialIndex = int(input("Выберите многочлен (номер): ")) - 1
        if polynomialIndex < 0 or polynomialIndex >= len(polynomialsList):
            print("Неверный номер")
            return

        inputValue = float(input("Введите значение x: "))
        selectedPolynomial = polynomialsList[polynomialIndex]
        resultValue = selectedPolynomial(inputValue)  # Используется оператор ()

        print(f"P({inputValue}) = {resultValue}")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def getCoefficientInteractive(polynomialsList):
    print("\n--- Получение коэффициентов многочлена (оператор []) ---")

    if not polynomialsList:
        print("Сначала создайте многочлены")
        return

    showPolynomials(polynomialsList)

    try:
        polynomialIndex = int(input("Выберите многочлен (номер): ")) - 1
        if polynomialIndex < 0 or polynomialIndex >= len(polynomialsList):
            print("Неверный номер")
            return

        selectedPolynomial = polynomialsList[polynomialIndex]
        print(f"Коэффициенты многочлена {selectedPolynomial}:")
        for currentIndex in range(selectedPolynomial.degree + 1):
            coefficientValue = selectedPolynomial[currentIndex]
            powerValue = selectedPolynomial.degree - currentIndex
            if powerValue == 0:
                print(f"  x^{powerValue} (свободный член): {coefficientValue}")
            else:
                print(f"  x^{powerValue}: {coefficientValue}")

    except ValueError:
        print("Ошибка ввода")

def addPolynomialsInteractive(polynomialsList):
    print("\n--- Сложение многочленов (оператор +) ---")
    print("Создает новый многочлен - сумму двух многочленов")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        firstIndex = int(input("Выберите первый многочлен (номер): ")) - 1
        secondIndex = int(input("Выберите второй многочлен (номер): ")) - 1

        if firstIndex < 0 or firstIndex >= len(polynomialsList) or secondIndex < 0 or secondIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        firstPolynomial = polynomialsList[firstIndex]
        secondPolynomial = polynomialsList[secondIndex]
        resultPolynomial = firstPolynomial + secondPolynomial  # Оператор + создает новый объект

        print(f"({firstPolynomial}) + ({secondPolynomial}) = {resultPolynomial}")
        polynomialsList.append(resultPolynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def iaddPolynomialsInteractive(polynomialsList):
    print("\n--- Сложение с присваиванием (оператор +=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        targetIndex = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        sourceIndex = int(input("Выберите многочлен для сложения: ")) - 1

        if targetIndex < 0 or targetIndex >= len(polynomialsList) or sourceIndex < 0 or sourceIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        targetPolynomial = polynomialsList[targetIndex]
        sourcePolynomial = polynomialsList[sourceIndex]

        print(f"До операции: {targetPolynomial}")
        targetPolynomial += sourcePolynomial
        print(f"После операции: {targetPolynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def subtractPolynomialsInteractive(polynomialsList):
    print("\n--- Вычитание многочленов (оператор -) ---")
    print("Создает новый многочлен - разность двух многочленов")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        firstIndex = int(input("Выберите первый многочлен (номер): ")) - 1
        secondIndex = int(input("Выберите второй многочлен (номер): ")) - 1

        if firstIndex < 0 or firstIndex >= len(polynomialsList) or secondIndex < 0 or secondIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        firstPolynomial = polynomialsList[firstIndex]
        secondPolynomial = polynomialsList[secondIndex]
        resultPolynomial = firstPolynomial - secondPolynomial

        print(f"({firstPolynomial}) - ({secondPolynomial}) = {resultPolynomial}")
        polynomialsList.append(resultPolynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def isubtractPolynomialsInteractive(polynomialsList):
    print("\n--- Вычитание с присваиванием (оператор -=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        targetIndex = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        sourceIndex = int(input("Выберите многочлен для вычитания: ")) - 1

        if targetIndex < 0 or targetIndex >= len(polynomialsList) or sourceIndex < 0 or sourceIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        targetPolynomial = polynomialsList[targetIndex]
        sourcePolynomial = polynomialsList[sourceIndex]

        print(f"До операции: {targetPolynomial}")
        targetPolynomial -= sourcePolynomial
        print(f"После операции: {targetPolynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def multiplyPolynomialsInteractive(polynomialsList):
    print("\n--- Умножение многочленов (оператор *) ---")
    print("Создает новый многочлен - произведение двух многочленов")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        firstIndex = int(input("Выберите первый многочлен (номер): ")) - 1
        secondIndex = int(input("Выберите второй многочлен (номер): ")) - 1

        if firstIndex < 0 or firstIndex >= len(polynomialsList) or secondIndex < 0 or secondIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        firstPolynomial = polynomialsList[firstIndex]
        secondPolynomial = polynomialsList[secondIndex]
        resultPolynomial = firstPolynomial * secondPolynomial

        print(f"({firstPolynomial}) * ({secondPolynomial}) = {resultPolynomial}")
        polynomialsList.append(resultPolynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def imultiplyPolynomialsInteractive(polynomialsList):
    print("\n--- Умножение с присваиванием (оператор *=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        targetIndex = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        sourceIndex = int(input("Выберите многочлен для умножения: ")) - 1

        if targetIndex < 0 or targetIndex >= len(polynomialsList) or sourceIndex < 0 or sourceIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        targetPolynomial = polynomialsList[targetIndex]
        sourcePolynomial = polynomialsList[sourceIndex]

        print(f"До операции: {targetPolynomial}")
        targetPolynomial *= sourcePolynomial
        print(f"После операции: {targetPolynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def dividePolynomialsInteractive(polynomialsList):
    print("\n--- Деление многочленов (оператор /) ---")
    print("Создает новый многочлен - частное от деления")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        dividendIndex = int(input("Выберите делимое (номер): ")) - 1
        divisorIndex = int(input("Выберите делитель (номер): ")) - 1

        if dividendIndex < 0 or dividendIndex >= len(polynomialsList) or divisorIndex < 0 or divisorIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        dividendPolynomial = polynomialsList[dividendIndex]
        divisorPolynomial = polynomialsList[divisorIndex]

        quotientPolynomial = dividendPolynomial / divisorPolynomial

        print(f"({dividendPolynomial}) / ({divisorPolynomial}) = {quotientPolynomial}")
        polynomialsList.append(quotientPolynomial)
        print("✓ Частное добавлено в список")

    except (ValueError, IndexError, ZeroDivisionError) as error:
        print(f" Ошибка: {error}")


def idividePolynomialsInteractive(polynomialsList):
    print("\n--- Деление с присваиванием (оператор /=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomialsList) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    showPolynomials(polynomialsList)

    try:
        targetIndex = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        divisorIndex = int(input("Выберите делитель: ")) - 1

        if targetIndex < 0 or targetIndex >= len(polynomialsList) or divisorIndex < 0 or divisorIndex >= len(polynomialsList):
            print("Неверные номера")
            return

        targetPolynomial = polynomialsList[targetIndex]
        divisorPolynomial = polynomialsList[divisorIndex]

        print(f"До операции: {targetPolynomial}")
        targetPolynomial /= divisorPolynomial
        print(f"После операции: {targetPolynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError, ZeroDivisionError) as error:
        print(f" Ошибка: {error}")


def showPolynomials(polynomialsList):
    print("\n--- Список многочленов ---")
    if not polynomialsList:
        print("Многочлены не созданы")
        return

    for index, polynomialItem in enumerate(polynomialsList, 1):
        print(f"{index}. {polynomialItem} (степень {polynomialItem.degree})")


def demoOperators():
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ВСЕХ ОПЕРАТОРОВ")
    print("=" * 50)

    firstPolynomial = Polynomial([2, -3, 1])  # 2x² - 3x + 1
    secondPolynomial = Polynomial([1, -1])     # x - 1

    print("1. Исходные многочлены:")
    print(f"   P1 = {firstPolynomial}")
    print(f"   P2 = {secondPolynomial}")

    print(f"\n2. Оператор [] - получение коэффициентов:")
    print(f"   P1[0] = {firstPolynomial[0]} (коэффициент при x²)")
    print(f"   P1[1] = {firstPolynomial[1]} (коэффициент при x)")
    print(f"   P1[2] = {firstPolynomial[2]} (свободный член)")

    print(f"\n3. Оператор () - вычисление значения:")
    print(f"   P1(0) = {firstPolynomial(0)}")
    print(f"   P1(1) = {firstPolynomial(1)}")
    print(f"   P1(2) = {firstPolynomial(2)}")

    sumPolynomial = firstPolynomial + secondPolynomial
    print(f"\n4. Оператор + - сложение (создает новый объект):")
    print(f"   ({firstPolynomial}) + ({secondPolynomial}) = {sumPolynomial}")
    print(f"   Исходный P1 не изменился: {firstPolynomial}")

    firstCopy = firstPolynomial.copy()
    originalFirst = str(firstCopy)
    firstCopy += secondPolynomial
    print(f"\n5. Оператор += - сложение с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {originalFirst}")
    print(f"   P1_copy += P2")
    print(f"   P1_copy изменился: {firstCopy}")

    diffPolynomial = firstPolynomial - secondPolynomial
    print(f"\n6. Оператор - - вычитание (создает новый объект):")
    print(f"   ({firstPolynomial}) - ({secondPolynomial}) = {diffPolynomial}")
    print(f"   Исходный P1 не изменился: {firstPolynomial}")

    firstCopy2 = firstPolynomial.copy()
    originalFirst2 = str(firstCopy2)
    firstCopy2 -= secondPolynomial
    print(f"\n7. Оператор -= - вычитание с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {originalFirst2}")
    print(f"   P1_copy -= P2")
    print(f"   P1_copy изменился: {firstCopy2}")

    productPolynomial = firstPolynomial * secondPolynomial
    print(f"\n8. Оператор * - умножение (создает новый объект):")
    print(f"   ({firstPolynomial}) * ({secondPolynomial}) = {productPolynomial}")
    print(f"   Исходный P1 не изменился: {firstPolynomial}")

    firstCopy3 = firstPolynomial.copy()
    originalFirst3 = str(firstCopy3)
    firstCopy3 *= secondPolynomial
    print(f"\n9. Оператор *= - умножение с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {originalFirst3}")
    print(f"   P1_copy *= P2")
    print(f"   P1_copy изменился: {firstCopy3}")

    quotientPolynomial = firstPolynomial / secondPolynomial
    print(f"\n10. Оператор / - деление (создает новый объект):")
    print(f"   ({firstPolynomial}) / ({secondPolynomial}) = {quotientPolynomial}")
    print(f"   Исходный P1 не изменился: {firstPolynomial}")

    firstCopy4 = firstPolynomial.copy()
    originalFirst4 = str(firstCopy4)
    firstCopy4 /= secondPolynomial
    print(f"\n11. Оператор /= - деление с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {originalFirst4}")
    print(f"   P1_copy /= P2")
    print(f"   P1_copy изменился: {firstCopy4}")

    print(f"\n12. Итоговое состояние исходных многочленов:")
    print(f"   P1 остался неизменным: {firstPolynomial}")
    print(f"   P2 остался неизменным: {secondPolynomial}")


def main():
    polynomialsList = []

    print("Программа для работы с многочленами")
    print("Создано несколько демонстрационных многочленов")

    polynomialsList.extend([
        Polynomial([2, -3, 1]),  # 2x² - 3x + 1
        Polynomial([1, -1]),  # x - 1
        Polynomial([1, 0, 1]),  # x² + 1
        Polynomial([3])  # 3
    ])

    while True:
        displayMenu()
        choice = input("Выберите действие (0-13): ").strip()

        menuActions = {
            '1': lambda: createPolynomialInteractive(polynomialsList),
            '2': lambda: evaluatePolynomialInteractive(polynomialsList),
            '3': lambda: getCoefficientInteractive(polynomialsList),
            '4': lambda: addPolynomialsInteractive(polynomialsList),
            '5': lambda: iaddPolynomialsInteractive(polynomialsList),
            '6': lambda: subtractPolynomialsInteractive(polynomialsList),
            '7': lambda: isubtractPolynomialsInteractive(polynomialsList),
            '8': lambda: multiplyPolynomialsInteractive(polynomialsList),
            '9': lambda: imultiplyPolynomialsInteractive(polynomialsList),
            '10': lambda: dividePolynomialsInteractive(polynomialsList),
            '11': lambda: idividePolynomialsInteractive(polynomialsList),
            '12': lambda: showPolynomials(polynomialsList),
            '13': lambda: demoOperators(),
            '0': lambda: exit()
        }

        if choice in menuActions:
            try:
                menuActions[choice]()
            except Exception as error:
                print(f" Произошла ошибка: {error}")
        else:
            print(" Неверный выбор! Пожалуйста, выберите действие от 0 до 13.")


if __name__ == "__main__":
    main()
