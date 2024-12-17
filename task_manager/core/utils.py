from re import sub as re_sub


def to_snake_case(text: str) -> str:
    """Преобразовывает CamelCase в snake_case.

    Добавляет нижнее подчеркивание перед заглавными буквами, кроме первой
    буквы строки. После этого превращает все буквы в строчные и
    возвращает строку.
    """

    return re_sub(r'(?<!^)(?=[A-Z])', '_', text).lower()
