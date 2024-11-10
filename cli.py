import sys
import subprocess

from app import compile

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERRO: Informe o arquivo a ser compilado! (ex. python run.py program.fei)')
        sys.exit()

    tokens, tree, translation = compile(sys.argv[1])

    new_file = f"{sys.argv[1]}.py"

    with open(new_file, "w") as f:
        f.write(translation)
    
    result = subprocess.run(["python", new_file])

    print(result.stdout)

    

