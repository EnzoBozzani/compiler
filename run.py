import sys

from models import SyntaticAnalysis, LexicalAnalysis, SemanticAnalysis


def main() -> None:
    if len(sys.argv) < 2:
        print('ERROR: Informe o arquivo a ser compilado! (ex. python run.py program.fei)')
        sys.exit()


    lexical_analyzer = LexicalAnalysis(sys.argv[1])

    syntatic_analyzer = SyntaticAnalysis(lexical_analyzer.tokens)

    syntatic_analyzer.tree.print_tree()

    # semantic_analyzer = SemanticAnalysis(syntatic_analyzer.trees)
        

if __name__ == '__main__':
    main()
