class Token():
    """
    Token class.

    Args:
        lexem: str
        type: str
    """
    __lexem: str
    __type: str

    def __init__(self, lexem: str, type: str) -> None:
        self.__lexem = lexem
        self.__type = type

    def getLexem(self) -> str:
        return self.__lexem

    def getType(self) -> str:
        return self.__type

    def to_string(self) -> str:
        return f"< {self.__type}, {self.__lexem} >"
