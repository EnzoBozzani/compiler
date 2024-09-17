from utils import is_word, word_matches_pattern
from models import Token

patterns: list[tuple[str, str]] = [
    ('if', 'if'),
    ('else', 'else'),
    ('number_reserved', 'number'),
    ('string_reserved', 'string'),
    ('while', 'while'),
    ('for', 'for'),
    ('in', 'in'),
    ('bool_reserved', 'bool'),
    ('true', 'true'),
    ('false', 'false'),
    ('semicolon', ';'),
    ('op', '('),
    ('cp', ')'),
    ('gt', '>'),
    ('attr', '='),
    ('equal', '=='),
    ('gte', '>='),
    ('lte', '<='),
    ('lt', '<'),
    ('open_curly_braces', '{'),
    ('close_curly_braces', '}'),
    ('string', '".*"'),
    ('number', '(0-9)+ | (0-9)*.(0-9)+'),
    ('id', '(a-z|A-Z)(a-z|A-Z|0-9|_)*'),
]

unique_patterns: list[tuple[str, str]] = [
    ('op', '('),
    ('cp', ')'),
    ('semicolon', ';'),
    ('open_curly_braces', '{'),
    ('close_curly_braces', '}'),
    ('attr', '=')
]


def main() -> None:
    words: list[str] = []

    with open('program.txt', 'r') as file:
        for line in file.readlines():
            for word in line.split(' '):
                words.append(word.strip())

    for i in range(len(words)):
        word = words[i]
        if (is_word(word)):
            for j in range(len(word)):
                char = word[j]
                for typ, pattern in unique_patterns:
                    if char == pattern:
                        words[i] = ''
                        for element in word.split(char):
                            words[i] += element
                        words.insert(i + 1, pattern)

    # for i in range(len(words)):
    #     if words[i] == '':
    #         words.pop(i)

    print(words)
    for word in words:
        for typ, pattern in patterns:
            if word_matches_pattern(word, pattern):
                print(Token(typ, word).to_string())


if __name__ == '__main__':
    main()
