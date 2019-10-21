
def get_spelling(num: int, ordinal: bool = True):
    if num > 0 and num % 100000 == 0:
        print(f'Spelling {num}')
    if num <= 12:
        return {
            0: '',
            1: 'first' if ordinal else 'one',
            2: 'second' if ordinal else 'two',
            3: 'third' if ordinal else 'three',
            4: 'fourth' if ordinal else 'four',
            5: 'fifth' if ordinal else 'five',
            6: 'sixth' if ordinal else 'six',
            7: 'seventh' if ordinal else 'seven',
            8: 'eighth' if ordinal else 'eight',
            9: 'ninth' if ordinal else 'nine',
            10: 'tenth' if ordinal else 'ten',
            11: 'eleventh' if ordinal else 'eleven',
            12: 'twelvth' if ordinal else 'twelve'
        }[num]
    if num < 20:
        return {
            13: 'thirteen',
            14: 'fourteen',
            15: 'fifteen',
            16: 'sixteen',
            17: 'seventeen',
            18: 'eighteen',
            19: 'nineteen'
        }[num] + 'th' if ordinal else ''

    if num < 100:
        first_digit = {
            2: 'twenty',
            3: 'thirty',
            4: 'fourty',
            5: 'fifty',
            6: 'sixty',
            7: 'seventy',
            8: 'eighty',
            9: 'ninety'
        }[num // 10]
        second_digit = get_spelling(num % 10, ordinal=ordinal)
        if second_digit == '':
            first_digit = first_digit[:-1] + 'ieth'
        return first_digit + second_digit

    if num < 1000:
        return get_spelling(num // 100, ordinal=False) + 'hundred' + get_spelling(num % 100, ordinal=ordinal)

    magnitudes = ['thousand', 'million', 'billion', 'trillion']
    for magnitude, power in zip(magnitudes, range(1, len(magnitudes) + 1)):
        bounds = 1000 ** power
        if bounds <= num < bounds * 1000:
            try:
                this_magnitude_spelling = get_spelling(
                    num // bounds, ordinal=False) + magnitude
                lower_magnitudes_spelling = get_spelling(
                    num % bounds, ordinal=ordinal)
                return (this_magnitude_spelling + lower_magnitudes_spelling) + ('th' if lower_magnitudes_spelling == '' else '')
            except TypeError:
                print(f'Error while getting spelling for {num}')


def generate_file_content(file, upper_bound=100):
    file.writelines([
        'library list_getters;\n\n',
        'extension <T> on List<T> ListGetters {\n',
        '  void _ensureThatIndexIsInBounds(String methodName, int index) {\n',
        '    if (index >= length) {\n',
        '      throw StateError(\n',
        '        \'You tried to call $methodName on a list that only has $length elements.\'\n',
        '      );\n',
        '    }\n',
        '  }\n',
        '\n',
        '  T _getElement(String methodName, int index) {\n',
        '    _ensureThatIndexIsInBounds(methodName, index);\n',
        '    return this[index];\n',
        '  }\n',
        '\n',
        '  void _setElement(String methodName, int index, T value) {\n',
        '    _ensureThatIndexIsInBounds(\'$methodName as a setter\', index);\n',
        '    this[index] = value;\n',
        '  }\n',
        '\n'
    ])
    for i in range(1, upper_bound):
        spelling = get_spelling(i + 1)
        file.writelines([
            f"  /// Returns the {spelling} element of the list.\n",
            f"  ///\n",
            f"  /// Equivalent to `theList[{i}]`.\n"
            f"  /// Throws a [StateError] if the list doesn't have a {spelling} element.\n",
            f"  T get {spelling} => _getElement('{spelling}', {i});\n",
            f"\n",
            f"  /// Updates the {spelling} position of the list to contain [value].\n",
            f"  ///\n",
            f"  /// Equivalent to `theList[{i}] = value`.\n"
            f" /// Throws a [StateError] if the list doesn't have a {spelling} element.\n",
            f"  T set {spelling}(T value) => _setElement('{spelling}', {i});\n",
            f"\n"
        ])
    for i in range(1, upper_bound):
        i += 1
        spelling = get_spelling(i)
        file.writelines([
            f"  /// Returns the {spelling} last element of the list.\n",
            f"  ///\n",
            f"  /// Equivalent to `theList[theList.length - {i}]`.\n"
            f"  /// Throws a [StateError] if the list doesn't have a {spelling} last element.\n",
            f"  T get {spelling}Last => _getElement('{spelling}Last', length - {i});\n",
            f"\n",
            f"  /// Updates the {spelling} last position of the list to contain [value].\n",
            f"  ///\n",
            f"  /// Equivalent to `theList[theList.length - {i}] = value`.\n"
            f"  /// Throws a [StateError] if the list doesn't have a {spelling} last element.\n",
            f"  T set {spelling}Last(T value) => _setElement('{spelling}Last', length - {i});\n",
            f"\n"
        ])
    file.write('}\n')


if __name__ == "__main__":
    with open('list_accessors.dart', 'w+') as file:
        generate_file_content(file, upper_bound=20)
