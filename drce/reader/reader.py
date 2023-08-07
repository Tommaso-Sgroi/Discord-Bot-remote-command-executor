import abc


class Reader(abc.ABC):
    def __init__(self):
        pass

    @abc.abstractmethod
    def read(self) -> str:
        raise NotImplementedError("Need to implement this method for correct behaviour")
