import abc
from typing import List


class BaseComparator(abc.ABC):
    @abc.abstractmethod
    def compare(self, mysql_result: List[str], target: List[str]) -> (List[int], List[int]):
        raise NotImplementedError
