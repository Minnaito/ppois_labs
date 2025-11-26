from src.Polynomial import polynomial


def display_menu():
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

def create_polynomial_interactive(polynomials_list):
    print("\n--- Создание многочлена ---")
    print("Примеры ввода:")
    print("  • 2x² - 3x + 1 → введите: 2 -3 1")
    print("  • x³ - 2x + 5 → введите: 1 0 -2 5")
    print("  • 4x + 7 → введите: 4 7")
    print("  • 5 → введите: 5")

    try:
        coefficients_input = input("\nВведите коэффициенты через пробел (старшая степень первая): ")
        coefficients_list = [float(number) for number in coefficients_input.split()]

        if not coefficients_list:
            print("Ошибка: не введены коэффициенты")
            return

        new_polynomial = polynomial(coefficients_list)
        polynomials_list.append(new_polynomial)
        print(f"✓ Создан многочлен: {new_polynomial}")
        print(f"✓ Степень: {new_polynomial.degree}")

    except ValueError:
        print(" Ошибка: введите только числа через пробел")
        print(" Например: '2 -3 1' для многочлена 2x² - 3x + 1")


def evaluate_polynomial_interactive(polynomials_list):
    print("\n--- Вычисление значения многочлена (оператор ()) ---")

    if not polynomials_list:
        print("Сначала создайте многочлены")
        return

    show_polynomials(polynomials_list)

    try:
        polynomial_index = int(input("Выберите многочлен (номер): ")) - 1
        if polynomial_index < 0 or polynomial_index >= len(polynomials_list):
            print("Неверный номер")
            return

        input_value = float(input("Введите значение x: "))
        selected_polynomial = polynomials_list[polynomial_index]
        result_value = selected_polynomial(input_value)  # Используется оператор ()

        print(f"P({input_value}) = {result_value}")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def get_coefficient_interactive(polynomials_list):
    print("\n--- Получение коэффициентов многочлена (оператор []) ---")

    if not polynomials_list:
        print("Сначала создайте многочлены")
        return

    show_polynomials(polynomials_list)

    try:
        polynomial_index = int(input("Выберите многочлен (номер): ")) - 1
        if polynomial_index < 0 or polynomial_index >= len(polynomials_list):
            print("Неверный номер")
            return

        selected_polynomial = polynomials_list[polynomial_index]
        print(f"Коэффициенты многочлена {selected_polynomial}:")
        for current_index in range(selected_polynomial.degree + 1):
            coefficient_value = selected_polynomial[current_index]
            power_value = selected_polynomial.degree - current_index
            if power_value == 0:
                print(f"  x^{power_value} (свободный член): {coefficient_value}")
            else:
                print(f"  x^{power_value}: {coefficient_value}")

    except ValueError:
        print("Ошибка ввода")

def add_polynomials_interactive(polynomials_list):
    print("\n--- Сложение многочленов (оператор +) ---")
    print("Создает новый многочлен - сумму двух многочленов")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        first_index = int(input("Выберите первый многочлен (номер): ")) - 1
        second_index = int(input("Выберите второй многочлен (номер): ")) - 1

        if first_index < 0 or first_index >= len(polynomials_list) or second_index < 0 or second_index >= len(polynomials_list):
            print("Неверные номера")
            return

        first_polynomial = polynomials_list[first_index]
        second_polynomial = polynomials_list[second_index]
        result_polynomial = first_polynomial + second_polynomial  # Оператор + создает новый объект

        print(f"({first_polynomial}) + ({second_polynomial}) = {result_polynomial}")
        polynomials_list.append(result_polynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def iadd_polynomials_interactive(polynomials_list):
    print("\n--- Сложение с присваиванием (оператор +=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        target_index = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        source_index = int(input("Выберите многочлен для сложения: ")) - 1

        if target_index < 0 or target_index >= len(polynomials_list) or source_index < 0 or source_index >= len(polynomials_list):
            print("Неверные номера")
            return

        target_polynomial = polynomials_list[target_index]
        source_polynomial = polynomials_list[source_index]

        print(f"До операции: {target_polynomial}")
        target_polynomial += source_polynomial
        print(f"После операции: {target_polynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def subtract_polynomials_interactive(polynomials_list):
    print("\n--- Вычитание многочленов (оператор -) ---")
    print("Создает новый многочлен - разность двух многочленов")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        first_index = int(input("Выберите первый многочлен (номер): ")) - 1
        second_index = int(input("Выберите второй многочлен (номер): ")) - 1

        if first_index < 0 or first_index >= len(polynomials_list) or second_index < 0 or second_index >= len(polynomials_list):
            print("Неверные номера")
            return

        first_polynomial = polynomials_list[first_index]
        second_polynomial = polynomials_list[second_index]
        result_polynomial = first_polynomial - second_polynomial

        print(f"({first_polynomial}) - ({second_polynomial}) = {result_polynomial}")
        polynomials_list.append(result_polynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def isubtract_polynomials_interactive(polynomials_list):
    print("\n--- Вычитание с присваиванием (оператор -=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        target_index = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        source_index = int(input("Выберите многочлен для вычитания: ")) - 1

        if target_index < 0 or target_index >= len(polynomials_list) or source_index < 0 or source_index >= len(polynomials_list):
            print("Неверные номера")
            return

        target_polynomial = polynomials_list[target_index]
        source_polynomial = polynomials_list[source_index]

        print(f"До операции: {target_polynomial}")
        target_polynomial -= source_polynomial
        print(f"После операции: {target_polynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def multiply_polynomials_interactive(polynomials_list):
    print("\n--- Умножение многочленов (оператор *) ---")
    print("Создает новый многочлен - произведение двух многочленов")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        first_index = int(input("Выберите первый многочлен (номер): ")) - 1
        second_index = int(input("Выберите второй многочлен (номер): ")) - 1

        if first_index < 0 or first_index >= len(polynomials_list) or second_index < 0 or second_index >= len(polynomials_list):
            print("Неверные номера")
            return

        first_polynomial = polynomials_list[first_index]
        second_polynomial = polynomials_list[second_index]
        result_polynomial = first_polynomial * second_polynomial

        print(f"({first_polynomial}) * ({second_polynomial}) = {result_polynomial}")
        polynomials_list.append(result_polynomial)
        print("✓ Новый многочлен добавлен в список")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def imultiply_polynomials_interactive(polynomials_list):
    print("\n--- Умножение с присваиванием (оператор *=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        target_index = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        source_index = int(input("Выберите многочлен для умножения: ")) - 1

        if target_index < 0 or target_index >= len(polynomials_list) or source_index < 0 or source_index >= len(polynomials_list):
            print("Неверные номера")
            return

        target_polynomial = polynomials_list[target_index]
        source_polynomial = polynomials_list[source_index]

        print(f"До операции: {target_polynomial}")
        target_polynomial *= source_polynomial
        print(f"После операции: {target_polynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError):
        print("Ошибка ввода")


def divide_polynomials_interactive(polynomials_list):
    print("\n--- Деление многочленов (оператор /) ---")
    print("Создает новый многочлен - частное от деления")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        dividend_index = int(input("Выберите делимое (номер): ")) - 1
        divisor_index = int(input("Выберите делитель (номер): ")) - 1

        if dividend_index < 0 or dividend_index >= len(polynomials_list) or divisor_index < 0 or divisor_index >= len(polynomials_list):
            print("Неверные номера")
            return

        dividend_polynomial = polynomials_list[dividend_index]
        divisor_polynomial = polynomials_list[divisor_index]

        quotient_polynomial = dividend_polynomial / divisor_polynomial

        print(f"({dividend_polynomial}) / ({divisor_polynomial}) = {quotient_polynomial}")
        polynomials_list.append(quotient_polynomial)
        print("✓ Частное добавлено в список")

    except (ValueError, IndexError, ZeroDivisionError) as error:
        print(f" Ошибка: {error}")


def idivide_polynomials_interactive(polynomials_list):
    print("\n--- Деление с присваиванием (оператор /=) ---")
    print("Изменяет левый многочлен, сохраняя в нем результат")

    if len(polynomials_list) < 2:
        print("Нужно как минимум 2 многочлена")
        return

    show_polynomials(polynomials_list)

    try:
        target_index = int(input("Выберите многочлен для изменения (будет изменен): ")) - 1
        divisor_index = int(input("Выберите делитель: ")) - 1

        if target_index < 0 or target_index >= len(polynomials_list) or divisor_index < 0 or divisor_index >= len(polynomials_list):
            print("Неверные номера")
            return

        target_polynomial = polynomials_list[target_index]
        divisor_polynomial = polynomials_list[divisor_index]

        print(f"До операции: {target_polynomial}")
        target_polynomial /= divisor_polynomial
        print(f"После операции: {target_polynomial}")
        print("✓ Левый многочлен изменен")

    except (ValueError, IndexError, ZeroDivisionError) as error:
        print(f" Ошибка: {error}")


def show_polynomials(polynomials_list):
    print("\n--- Список многочленов ---")
    if not polynomials_list:
        print("Многочлены не созданы")
        return

    for index, polynomial_item in enumerate(polynomials_list, 1):
        print(f"{index}. {polynomial_item} (степень {polynomial_item.degree})")


def demo_operators():
    print("\n" + "=" * 50)
    print("ДЕМОНСТРАЦИЯ РАБОТЫ ВСЕХ ОПЕРАТОРОВ")
    print("=" * 50)

    first_polynomial = polynomial([2, -3, 1])  # 2x² - 3x + 1
    second_polynomial = polynomial([1, -1])     # x - 1

    print("1. Исходные многочлены:")
    print(f"   P1 = {first_polynomial}")
    print(f"   P2 = {second_polynomial}")

    print(f"\n2. Оператор [] - получение коэффициентов:")
    print(f"   P1[0] = {first_polynomial[0]} (коэффициент при x²)")
    print(f"   P1[1] = {first_polynomial[1]} (коэффициент при x)")
    print(f"   P1[2] = {first_polynomial[2]} (свободный член)")

    print(f"\n3. Оператор () - вычисление значения:")
    print(f"   P1(0) = {first_polynomial(0)}")
    print(f"   P1(1) = {first_polynomial(1)}")
    print(f"   P1(2) = {first_polynomial(2)}")

    sum_polynomial = first_polynomial + second_polynomial
    print(f"\n4. Оператор + - сложение (создает новый объект):")
    print(f"   ({first_polynomial}) + ({second_polynomial}) = {sum_polynomial}")
    print(f"   Исходный P1 не изменился: {first_polynomial}")

    first_copy = first_polynomial.copy()
    original_first = str(first_copy)
    first_copy += second_polynomial
    print(f"\n5. Оператор += - сложение с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {original_first}")
    print(f"   P1_copy += P2")
    print(f"   P1_copy изменился: {first_copy}")

    diff_polynomial = first_polynomial - second_polynomial
    print(f"\n6. Оператор - - вычитание (создает новый объект):")
    print(f"   ({first_polynomial}) - ({second_polynomial}) = {diff_polynomial}")
    print(f"   Исходный P1 не изменился: {first_polynomial}")

    first_copy_2 = first_polynomial.copy()
    original_first_2 = str(first_copy_2)
    first_copy_2 -= second_polynomial
    print(f"\n7. Оператор -= - вычитание с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {original_first_2}")
    print(f"   P1_copy -= P2")
    print(f"   P1_copy изменился: {first_copy_2}")

    product_polynomial = first_polynomial * second_polynomial
    print(f"\n8. Оператор * - умножение (создает новый объект):")
    print(f"   ({first_polynomial}) * ({second_polynomial}) = {product_polynomial}")
    print(f"   Исходный P1 не изменился: {first_polynomial}")

    first_copy_3 = first_polynomial.copy()
    original_first_3 = str(first_copy_3)
    first_copy_3 *= second_polynomial
    print(f"\n9. Оператор *= - умножение с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {original_first_3}")
    print(f"   P1_copy *= P2")
    print(f"   P1_copy изменился: {first_copy_3}")

    quotient_polynomial = first_polynomial / second_polynomial
    print(f"\n10. Оператор / - деление (создает новый объект):")
    print(f"   ({first_polynomial}) / ({second_polynomial}) = {quotient_polynomial}")
    print(f"   Исходный P1 не изменился: {first_polynomial}")

    first_copy_4 = first_polynomial.copy()
    original_first_4 = str(first_copy_4)
    first_copy_4 /= second_polynomial
    print(f"\n11. Оператор /= - деление с присваиванием (изменяет левый объект):")
    print(f"   P1_copy = {original_first_4}")
    print(f"   P1_copy /= P2")
    print(f"   P1_copy изменился: {first_copy_4}")

    print(f"\n12. Итоговое состояние исходных многочленов:")
    print(f"   P1 остался неизменным: {first_polynomial}")
    print(f"   P2 остался неизменным: {second_polynomial}")


def main():
    polynomials_list = []

    print("Программа для работы с многочленами")
    print("Создано несколько демонстрационных многочленов")

    polynomials_list.extend([
        polynomial([2, -3, 1]),  # 2x² - 3x + 1
        polynomial([1, -1]),  # x - 1
        polynomial([1, 0, 1]),  # x² + 1
        polynomial([3])  # 3
    ])

    while True:
        display_menu()
        choice = input("Выберите действие (0-13): ").strip()

        menu_actions = {
            '1': lambda: create_polynomial_interactive(polynomials_list),
            '2': lambda: evaluate_polynomial_interactive(polynomials_list),
            '3': lambda: get_coefficient_interactive(polynomials_list),
            '4': lambda: add_polynomials_interactive(polynomials_list),
            '5': lambda: iadd_polynomials_interactive(polynomials_list),
            '6': lambda: subtract_polynomials_interactive(polynomials_list),
            '7': lambda: isubtract_polynomials_interactive(polynomials_list),
            '8': lambda: multiply_polynomials_interactive(polynomials_list),
            '9': lambda: imultiply_polynomials_interactive(polynomials_list),
            '10': lambda: divide_polynomials_interactive(polynomials_list),
            '11': lambda: idivide_polynomials_interactive(polynomials_list),
            '12': lambda: show_polynomials(polynomials_list),
            '13': lambda: demo_operators(),
            '0': lambda: exit()
        }

        if choice in menu_actions:
            try:
                menu_actions[choice]()
            except Exception as error:
                print(f" Произошла ошибка: {error}")
        else:
            print(" Неверный выбор! Пожалуйста, выберите действие от 0 до 13.")


if __name__ == "__main__":
    main()
