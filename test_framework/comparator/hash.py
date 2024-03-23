from typing import List
from test_framework.comparator.base import BaseComparator


class HashComparator(BaseComparator):
    def __init__(self):
        super().__init__()

    def compare(self, mysql_result: List[str], target: List[str]) -> (List[int], List[int], Exception):
        mysql_hash = set((idx, hash(row)) for idx, row in enumerate(mysql_result))
        target_hash = set((idx, hash(row)) for idx, row in enumerate(target))

        if len(mysql_hash) != len(target_hash):
            return None, None, Exception("row number mismatch")

        matched_row = []
        unmatched_row = []
        for idx, hash_value in mysql_hash:
            if (idx, hash_value) in target_hash:
                matched_row.append(idx)
            else:
                unmatched_row.append(idx)

        return matched_row, unmatched_row, None
