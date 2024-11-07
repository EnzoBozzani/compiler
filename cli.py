import sys

from app import compile

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('ERROR: Informe o arquivo a ser compilado! (ex. python run.py program.fei)')
        sys.exit()
    compile(sys.argv[1])