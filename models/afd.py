from abc import ABC, abstractmethod
from models import Token


class AFD(ABC):
    @abstractmethod
    def evaluate(self) -> Token:
        raise NotImplementedError('Not implemented')
