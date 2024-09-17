from utils import is_word

regex = {
    'id': r"^[a-zA-Z][a-zA-Z0-9_]*$",
    'number_reserved': r"^number$"
}


def main() -> None:
    words: list[str] = []

    with open('program.txt', 'r') as file:
        for line in file.readlines():
            for word in line.split(' '):
                words.append(word.strip())

    for word in words:
        print(f"word: {word} - is_word: {is_word(word)}")


if __name__ == '__main__':
    main()
