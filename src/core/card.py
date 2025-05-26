from abc import ABC, abstractmethod

class Card(ABC):
    @abstractmethod
    def __str__(self) -> str:
        pass

    def __repr__(self) -> str:
        return str(self)