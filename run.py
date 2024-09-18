from utils import word_matches_pattern, extract_words_from_program
from models import Token
from constants import patterns


def main() -> None:
    words = extract_words_from_program('program.txt')

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
