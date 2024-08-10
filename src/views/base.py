import abc

from config import ViewName
from gtk import BasicGTK


class View(abc.ABC):
    @property
    @abc.abstractmethod
    def name(self) -> ViewName:
        pass

    @abc.abstractmethod
    def draw(self, gtk: BasicGTK) -> None:
        pass
