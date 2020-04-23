from abc import (
    ABC,
    abstractmethod
)


class AbstractDataMgmt(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs):
        pass