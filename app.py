import sys
import subprocess

from models import SyntaticAnalysis, LexicalAnalysis, SemanticAnalysis


def compile(arg):
    lexical_analyzer = LexicalAnalysis(arg)

    tokens_output = [t.to_string() for t in lexical_analyzer.tokens]

    syntatic_analyzer = SyntaticAnalysis(lexical_analyzer.tokens)

    semantic_analyzer = SemanticAnalysis(syntatic_analyzer.tree.root)

    return tokens_output, syntatic_analyzer.tree, semantic_analyzer.translation

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERRO: Informe o arquivo a ser compilado! (ex. python run.py program.fei)')
        sys.exit()

    tokens, tree, translation = compile(sys.argv[1])

    new_file = f"{sys.argv[1]}.py"

    with open(new_file, "w") as f:
        f.write(translation)
    
    subprocess.run(["python", new_file])