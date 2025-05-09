from abc import ABC, abstractmethod
from typing import List

class BaseGenerator(ABC):

    def generate(self, question: str, docs: List[str]) -> str:

        pass
