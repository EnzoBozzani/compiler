from models import Token
from constants import grammar

class SyntaticAnalysis():
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens

        # l = range(len(self.tokens))

        # for _ in l:
        #     token = self.nextToken()
        #     for rule in grammar:
        #         for i, option in enumerate(grammar[rule]):
        #             if token.getType() == option:
        #                 token = self.nextToken()

        # print(self.belongs_to_rule('math_expression', 
        #     [
        #         Token('number', '10'),
        #         Token('add', '+'),
        #         Token('id', 'a'),
        #         Token('add', '+'),
        #         Token('op', '('),
        #         Token('number', '3'),
        #         Token('add', '+'),
        #         Token('number', '6'),
        #         Token('cp', ')')
        #     ]
        # ))

        print(self.belongs_to_rule('math', 
            [
                Token('op', '('),
                Token('number', '10'),
                Token('add', '+'),
                Token('id', 'a'),
                Token('add', '+'),
                Token('op', '('),
                Token('number', '3'),
                Token('add', '+'),
                Token('number', '6'),
                Token('cp', ')'),
                Token('cp', ')')
            ]
        ))
                        

    def nextToken(self):
        return self.tokens.pop(0)
    
    def belongs_to_rule(self, rule: str, seq: list[Token]):
        rule_arr = rule.split(' ')

        for i, regex in enumerate(rule_arr):

            print(seq[i].to_string())
            print(regex)

            if regex in grammar:
                valid = True
                for option in grammar[regex]:
                    if (not self.belongs_to_rule(option, seq[i:])):
                        valid = False
                    else:
                        valid = True
                        break
            
                if not valid:
                    return False        
            elif regex != seq[i].getType():
                return False

        return True