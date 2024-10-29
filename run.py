import sys

from lexical import lexical_analysis
from models import SyntaticAnalysis


def main() -> None:
    if len(sys.argv) < 2:
        raise Exception('Pass the file to be compiled as last parameter! (e.g. python run.py program.fei)')

    tokens = lexical_analysis(sys.argv[1])

    syntatic_analyzer = SyntaticAnalysis(tokens)
        

if __name__ == '__main__':
    main()
