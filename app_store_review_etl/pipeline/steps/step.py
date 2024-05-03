from abc import ABC
from abc import abstractmethod


class Step(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def process(self, gspread_client, inputs):
        pass


class StepException(Exception):
    pass
