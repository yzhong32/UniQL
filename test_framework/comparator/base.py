import abc
from typing import List


class QueryComparator(abc.ABC):
    @abc.abstractmethod
    def compare(self, mysql_result: List[str], target: List[str]) -> (List[int], List[int], Exception):
        raise NotImplementedError
