az_list = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
az_upper_list = [char.upper() for char in az_list]
numbers_list = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']


def is_word(string: str):
    return len(string) > 1


def belongs_to_az(char: str) -> bool:
    return char in az_list


def belongs_to_az_upper(char: str) -> bool:
    return char in az_upper_list


def belongs_to_numbers(char: str) -> bool:
    return char in numbers_list


def char_belongs_to_group(char: str, group: list[str]) -> bool:
    for element in group:
        if element == 'a-z':
            if belongs_to_az(char):
                return True
        elif element == 'A-Z':
            if belongs_to_az_upper(char):
                return True
        elif element == '0-9':
            if belongs_to_numbers(char):
                return True
        elif element == '*' or element == '+':
            pass
        else:
            if char == element:
                return True

    return False
