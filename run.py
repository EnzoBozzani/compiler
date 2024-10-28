import sys

from lexical import lexical_analysis
from syntatic import syntatic_analysis


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception('Pass the file to be compiled as last parameter! (e.g. python run.py program.fei)')

    tokens = lexical_analysis(sys.argv[1])

    tree = syntatic_analysis(tokens)
        

if __name__ == '__main__':
    main()
