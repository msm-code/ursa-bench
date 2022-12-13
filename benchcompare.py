import json
import argparse
from os import read
from pathlib import Path
import re
from typing import Dict
from util import BenchmarkResult, Statistics


def parse_benchmark_results(file: Path) -> Dict[str, BenchmarkResult]:
    result = {}
    for line in file.read_text().split("\n"):
        if not line:
            continue

        rawdata = json.loads(line)
        name = rawdata["filename"]
        status = rawdata["status"]
        message = rawdata["message"]
        stats = Statistics(**rawdata["stats"]) if rawdata["stats"] else None
        result[name] = BenchmarkResult(status, message, stats)

    return result


def main() -> None:
    parser = argparse.ArgumentParser(description="UrsaDB benchmark suite.")
    parser.add_argument("left", help="First benchmark result to compare")
    parser.add_argument("right", help="Second benchmark result to compare")
    args = parser.parse_args()

    left = parse_benchmark_results(Path(args.left))
    right = parse_benchmark_results(Path(args.right))

    for filename, lvalue in left.items():
        if filename not in right:
            print(f"{filename}: missing in right")
            continue
        
        rvalue = right[filename]
        if lvalue.status != rvalue.status:
            print(f"{filename}: was {lvalue.status} and is {rvalue.status}")
            continue

        if rvalue.stats is None:
            continue

        lstats, rstats = lvalue.stats, rvalue.stats
        assert lstats is not None and rstats is not None
        diffs = ""
        # for op in ["and", "or", "minof", "read", "file"]:
        for op in ["read", "file"]:
        # for op in ["file"]:
            if lstats[f"{op}_count"] != rstats[f"{op}_count"]:
                l = lstats[f"{op}_count"]
                r = rstats[f"{op}_count"]
                val = r - l
                val = (r-l) / (l + 0.001)
                diffs += f"{op}: {l} vs {r} ({val:%}) "

        if not diffs:
            continue

        print(f"{filename}: {diffs}")

if __name__ == "__main__":
    main()
