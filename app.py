from models import SyntaticAnalysis, LexicalAnalysis, SemanticAnalysis


def compile(arg):
    lexical_analyzer = LexicalAnalysis(arg)

    tokens_output = [t.to_string() for t in lexical_analyzer.tokens]

    syntatic_analyzer = SyntaticAnalysis(lexical_analyzer.tokens)

    semantic_analyzer = SemanticAnalysis(syntatic_analyzer.tree.root)

    return tokens_output, syntatic_analyzer.tree, semantic_analyzer.translation