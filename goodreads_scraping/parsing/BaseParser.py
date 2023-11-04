from abc import ABC, abstractmethod


class BaseParser(ABC):
    @abstractmethod
    def get_xpath(self) -> str:
        ...

    @abstractmethod
    def parse(self, text: str) -> str:
        ...
