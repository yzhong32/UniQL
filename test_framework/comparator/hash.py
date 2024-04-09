from typing import List
from test_framework.comparator.base import QueryComparator


class HashComparator(QueryComparator):
    def __init__(self):
        super().__init__()

    def compare(self, mysql_result: List[str], target: List[str]) -> (bool, List[int], Exception):
        mysql_hash = {hash(row): idx for idx, row in enumerate(mysql_result)}
        target_hash = {hash(row): idx for idx, row in enumerate(target)}

        if len(mysql_result) != len(target):
            return None, None, Exception("Row number mismatch")

        unmatched = []

        for row_hash, idx in mysql_hash.items():
            if row_hash not in target_hash:
                unmatched.append(idx)

        return len(unmatched) == 0, unmatched, None


if __name__ == '__main__':
    cmp = HashComparator()
    matched_row, unmatched_row, e = cmp.compare(["bohan", "feize"], ["feize", "bohan"])

    print(f"Matched Rows: {matched_row}")
    print(f"Unmatched Rows: {unmatched_row}")
    if e:
        print(f"Error: {e}")
