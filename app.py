import uuid

from fastapi import FastAPI, UploadFile

from models import SyntaticAnalysis, LexicalAnalysis, SemanticAnalysis


def compile(arg):
    lexical_analyzer = LexicalAnalysis(arg)

    syntatic_analyzer = SyntaticAnalysis(lexical_analyzer.tokens)

    semantic_analyzer = SemanticAnalysis()

    semantic_analyzer.analyze(syntatic_analyzer.tree.root)

    return lexical_analyzer.tokens, syntatic_analyzer.tree
        
app = FastAPI()

@app.post("/")
async def root(file: UploadFile):
    id = uuid.uuid4()

    with open(f"./temp/{id}", 'wb') as f:   
        buffer = await file.read()
        f.write(buffer)
    
    tokens, tree = compile(f"./temp/{id}")

    return {
        "tokens": tokens,
        "tree": tree
    }