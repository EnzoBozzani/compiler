import sys

from models import Token
from constants import patterns, unique_patterns
from utils import char_belongs_to_group, is_word

class LexicalAnalysis():
    tokens: list[Token]
    def __init__(self, file: str):
        words = self.extract_words_from_program(file)

        start = None
        end = None
        for i, word in enumerate(words):
            if word.startswith('"'):
                start = i 
                for j in range(i, len(words)):
                    if words[j].endswith('"'):
                        end = j
                        break
                break
        if start != None:
            full_word = ""
            count = 0
            for i in range(start, end + 1):
                full_word += f"{words[i - count]} "
                words.pop(i - count)
                count += 1
            
            words.insert(start, full_word.strip())
        

        tokens: list[Token] = []

        for word in words:
            token_recognized = False
            for typ, pattern in patterns:
                if ' | ' in pattern:
                    for subpattern in pattern.split(' | '):
                        token_recognized = self.word_matches_pattern(word, subpattern)
                        if token_recognized:
                            break
                else:
                    token_recognized = self.word_matches_pattern(word, pattern)  
                if token_recognized:
                    tokens.append(Token(typ, word))
                    break   
            if not token_recognized:
                print(f"ERRO LÉXICO: Token não reconhecido: '{word}'")
                sys.exit()
                
        self.tokens: list[Token] = tokens

    def word_matches_pattern(self, word_to_be_matched: str, pattern: str) -> bool:
        groups: list[list[str]] = []

        word = word_to_be_matched

        if word.startswith('"') and word.endswith('"') and pattern == '".*"':
            return True

        if len(pattern) == 1:
            return word == pattern

        # normalization start
        group_start = 0
        group_end = len(pattern)

        for i in range(len(pattern)):
            char = pattern[i]

            if char == '(':
                group_start = i + 1
                group_end = len(pattern)
            elif char == ')':
                group_end = i
                group_raw = pattern[group_start:i]

                if pattern[i + 1] == '*' or pattern[i + 1] == '+':
                    group_raw += pattern[i + 1]

                    i += 1

                group = group_raw.split('|')

                for i in range(len(group)):
                    if '*' in group[i]:
                        group[i] = group[i][:len(group[i]) - 1]
                        group.append('*')
                    if '+' in group[i]:
                        group[i] = group[i][:len(group[i]) - 1]
                        group.append('+')

                groups.append(group)
            elif (not (i < group_end and i > group_start - 1)) and (char != '*' and char != '+'):
                groups.append([char])

        if (len(groups) == 0):
            for char in pattern:
                groups.append([char])
        # normalization end

        for arr in groups:
            if arr[-1] == '*':
                for char in word:
                    if char_belongs_to_group(char, arr):
                        word = word[1:]
                    else:
                        break
            elif arr[-1] == '+':
                for char in word:
                    if char_belongs_to_group(char, arr):
                        word = word[1:]
                    else:
                        return False
            else:
                if len(word) == 0:
                    return False
                char = word[0]
                if char_belongs_to_group(char, arr):
                    word = word[1:]
                else:
                    return False

        return len(word) == 0


    def extract_words_from_program(self, filename: str) -> list[str]:
        words: list[str] = []

        with open(filename, 'r') as file:
            for line in file.readlines():
                for word in line.split(' '):
                    words.append(word.strip())

        count = len(words)
        for i in range(count):
            word = words[i]
            if (is_word(word)):
                new_word = ''
                word_split: list[str] = []
                for j in range(len(word)):
                    char = word[j]
                    char_belongs_to_pattern = False
                    for _, pattern in unique_patterns:
                        if char == pattern:
                            char_belongs_to_pattern = True
                            break

                    if char == '(':
                        word_split.append(char)
                        word_split.append(word[1:])
                        new_word_split = [char]
                        changed = False
                        for word_split_index, new_char in enumerate(word_split[1]):
                            if new_char in [u for _, u in unique_patterns]:
                                if word_split[1][:word_split_index] == new_char:
                                    new_word_split.append(word_split[1][:word_split_index])
                                else:
                                    new_word_split.append(word_split[1][:word_split_index])
                                    new_word_split.append(new_char)
                                word_split[1] = word_split[1][word_split_index + 1:]
                                changed = True
                        
                        word_split = [a for a in new_word_split] if changed else [a for a in word_split]
                        break
                            
                    elif char_belongs_to_pattern:
                        if new_word != '':
                            word_split.append(new_word)
                            new_word = ''
                        word_split.append(char)
                    else:
                        new_word += char

                if len(word_split) >= 1:
                    words.pop(i)
                    count -= 1
                    for index in range(len(word_split)):
                        words.insert(i + index, word_split[index])
                        count += 1

        count = 0
        while (count < len(words)):
            if words[count] == '':
                words.pop(count)
                count -= 1
            count += 1

        count = len(words)
        for i in range(count):
            word = words[i]

            if (i + 1 >= count):
                break

            next_word = words[i + 1]

            if word == '>' and next_word == '=':
                words[i] = '>='
                words.pop(i + 1)
                count -= 1

            elif word == '<' and next_word == '=':
                words[i] = '<='
                words.pop(i + 1)
                count -= 1

            elif word == '=' and next_word == '=':
                words[i] = '=='
                words.pop(i + 1)
                count -= 1
            
            elif word == 'i' and next_word == 'n':
                words[i] = '=='
                words.pop(i + 1)
                count -= 1

        return words


         