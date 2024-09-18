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
    ('add', '+'),
    ('sub', '-'),
    ('mult', '*'),
    ('div', '/'),
    ('number', '(0-9)+ | (0-9)*.(0-9)+'),
    ('id', '(a-z|A-Z)(a-z|A-Z|0-9|_)*')
]

unique_patterns: list[tuple[str, str]] = [
    ('op', '('),
    ('cp', ')'),
    ('add', '+'),
    ('sub', '-'),
    ('mult', '*'),
    ('div', '/'),
    ('open_curly_braces', '{'),
    ('close_curly_braces', '}'),
    ('gt', '>'),
    ('attr', '='),
    ('equal', '=='),
    ('gte', '>='),
    ('lte', '<='),
    ('lt', '<'),
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

    count = 0
    while (count < len(words)):
        if words[count] == '':
            words.pop(count)
            count -= 1
        count += 1

    print(words)
    for word in words:
        token_recognized = False
        for typ, pattern in patterns:
            if ' | ' in pattern:
                for subpattern in pattern.split(' | '):
                    token_recognized = word_matches_pattern(word, subpattern)
                    if token_recognized:
                        break
            else:
                token_recognized = word_matches_pattern(word, pattern)

            if token_recognized:
                print(Token(typ, word).to_string())
                break

        if not token_recognized:
            raise Exception(f"Token not recognized: '{word}'")


if __name__ == '__main__':
    main()
