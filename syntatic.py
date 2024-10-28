from models import Token
from constants import grammar

def syntatic_analysis(tokens: list[Token]):

    # for token in tokens:
    for rule in grammar:
        for option in grammar[rule]:
            print(option)

    return {}