# from utils import is_word
# from models import Token

regex = {
    'id': "(a-z|A-Z)(a-z|A-Z|0-9|_)*",
    'number_reserved': "number"
}

unique_regex: list[tuple[str, str]] = [
    ('op', '('),
    ('cp', ')'),
    ('semicolon', ';'),
    ('open_curly_braces', '{'),
    ('close_curly_braces', '}')
]


def main() -> None:
    words: list[str] = []

    with open('program.txt', 'r') as file:
        for line in file.readlines():
            for word in line.split(' '):
                words.append(word.strip())

    # for word in words:

    #     if (is_word(word)):
    #         for char in word:
    #             for type, regex in unique_regex:
    #                 if char == regex:
    #                     print(char)
    #     else:
    #         for type, regex in regex:


if __name__ == '__main__':
    main()
