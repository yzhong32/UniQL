from typing import List
from test_framework.comparator.base import BaseComparator


class HashComparator(BaseComparator):
    def __init__(self):
        super().__init__()

    def compare(self, mysql_result: List[str], target: List[str]) -> (List[int], List[int], Exception):
        mysql_hash = set(hash(row) for row in mysql_result)
        target_hash = set(hash(row) for row in target)

        if len(mysql_result) != len(target):
            return None, None, Exception("Row number mismatch")

        matched_row = []
        unmatched_row = []

        for idx, row in enumerate(mysql_result):
            if hash(row) in target_hash:
                matched_row.append(idx)
            else:
                unmatched_row.append(idx)

        return matched_row, unmatched_row, None

if __name__ == '__main__':
    cmp = HashComparator()
    matched_row, unmatched_row, e = cmp.compare(["bohan", "feize"], ["feize", "bohan"])

    print(f"Matched Rows: {matched_row}")
    print(f"Unmatched Rows: {unmatched_row}")
    if e:
        print(f"Error: {e}")
