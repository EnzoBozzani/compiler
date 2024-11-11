import sys
import subprocess
from time import sleep

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
    
    option = ""
    while (option != "5"):
        sleep(1)
        option = input("\n1. Exibir tokens\n2. Exibir AST\n3. Exibir tradução pra Python\n4. Executar arquivo python gerado\n5. Sair\nOpção: ")
        print()
        if option == "1":
            for t in tokens:
                print(t)
        elif option == "2":
            tree.print_tree()
        elif option == "3":
            print(translation)
        elif option == "4":
            subprocess.run(["python", new_file])
        elif option == "5":
            print("Obrigado por utilizar!")
        else:
            print("Selecione uma opção válida")
        