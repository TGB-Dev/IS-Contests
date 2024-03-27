import csv
import argparse

class Random:
    """Random number generator based on testlib"""

    seed = 3905348978240129619
    multiplier = 0x5DEECE66D
    addend = 0xB
    mask = (1 << 48) - 1
    INT_MAX = 2147483647

    def nextBits(self, bits: int) -> int:
        assert bits <= 48, "bits must be <= 48"
        self.seed = (self.seed * self.multiplier + self.addend) & self.mask
        return self.seed >> (48 - bits)

    def setSeed(self, _seed: int) -> None:
        """Sets seed by given integer"""
        _seed = (_seed ^ self.multiplier) & self.mask
        self.seed = _seed

    def next(self, n: int) -> int:
        """Returns random integer in range [0, n - 1]"""
        assert n > 0, "n must be positive"
        assert n < self.INT_MAX, "n must be less than INT_MAX"

        if (n & -n) == n:  # n is a power of 2
            return (n * self.nextBits(31)) >> 31

        limit = self.INT_MAX / n * n
        bits = self.nextBits(31)
        while bits >= limit:
            bits = self.nextBits(31)

        return bits % n

    def nextRange(self, low: int, high: int) -> int:
        """Returns random integer in range [low, high]"""
        return self.next(high - low + 1) + low

def main():
    parser = argparse.ArgumentParser(description='Get TGB Contest 1 winners')
    parser.add_argument('csv', type=str, help='Path to CSV file')
    parser.add_argument('seed', type=int, help='Random seed')
    args = parser.parse_args()

    with open(args.csv, 'r', encoding='utf8') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    candidates = {}
    for row in rows:
        total_points = float(row["Points"])
        if (total_points > 0):
            candidates[row["Username"]] = total_points


    rnd = Random()
    rnd.setSeed(args.seed)
    winners = []
    for _ in range(4):
        names = list(candidates.keys())
        id = rnd.next(len(names))
        winners.append(names[id])
        candidates.pop(names[id])

    assert len(winners) == 4

    print('\n'.join(winners))


if __name__ == "__main__":
    main()
