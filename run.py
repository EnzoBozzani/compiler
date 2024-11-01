import sys

from models import SyntaticAnalysis, LexicalAnalysis


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception('Informe o arquivo a ser compilado! (ex. python run.py program.fei)')

    lexical = LexicalAnalysis(sys.argv[1])

    syntatic_analyzer = SyntaticAnalysis(lexical.tokens)

        

if __name__ == '__main__':
    main()
