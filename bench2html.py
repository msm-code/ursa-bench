import json
import argparse
from pathlib import Path
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


def get_style(prev: BenchmarkResult, next: BenchmarkResult) -> str:
    if next.status != "success":
        return "background-color: #eeeeee;"
    if prev.status != "success":
        return "background-color: #88ff88;"
    ns = next.stats
    ps = prev.stats

    if ns["file_count"] != ps["file_count"]:
        return "background-color: #ff8888;"

    if ns["read_count"] != ps["read_count"]:
        if ns["read_count"] < ps["read_count"]:
            return "background-color: #88ff88;"
        else:
            return "background-color: #ffff88;"

    return "background-color: #ffffff;"


def main() -> None:
    parser = argparse.ArgumentParser(description="UrsaDB benchmark suite.")
    parser.add_argument("filenames", nargs="*", help="List of benchmark result files")
    args = parser.parse_args()

    results: Dict[str, Dict[str, BenchmarkResult]] = {}
    for datafile in args.filenames:
        results[datafile] = parse_benchmark_results(Path(datafile))

    key_ordered_set = list(next(x for x in results.values()).keys())

    totals = {datafile: Statistics(
        and_count=0,
        and_milliseconds=0,
        minof_count=0,
        minof_milliseconds=0,
        or_count=0,
        or_milliseconds=0,
        read_count=0,
        read_milliseconds=0,
        file_count=0,
    ) for datafile in args.filenames}

    print("<html>")
    print("<table style=\"border: 1px solid\">")
    print("<tr>")
    print(f"<th>rule</th>")
    for datafile in args.filenames:
        print(f"<th style=\"border: 1px solid\">{Path(datafile).name}</th>")
    print("</tr>")
    for key in key_ordered_set:
        print("<tr>")
        print(f"<td style=\"border: 1px solid\">{key}</td>")
        prev = None
        for datafile in args.filenames:
            if datafile not in results or key not in results[datafile]:
                print(f"<td></td>")
                continue
            style = get_style(prev or results[datafile][key], results[datafile][key])
            print(f"<td style=\"border: 1px solid; {style}\">{results[datafile][key].short_format()}</td>")
            prev = results[datafile][key]
            stats = results[datafile][key].stats
            if stats is not None:
                totals[datafile]["and_count"] += stats["and_count"]
                totals[datafile]["and_milliseconds"] += stats["and_milliseconds"]
                totals[datafile]["minof_count"] += stats["minof_count"]
                totals[datafile]["minof_milliseconds"] += stats["minof_milliseconds"]
                totals[datafile]["or_count"] += stats["or_count"]
                totals[datafile]["or_milliseconds"] += stats["or_milliseconds"]
                totals[datafile]["read_count"] += stats["read_count"]
                totals[datafile]["read_milliseconds"] += stats["read_milliseconds"]
                totals[datafile]["file_count"] += stats["file_count"]


        print("</tr>")
    print("<tr>")
    print(f"<td style=\"border: 1px solid\"><b>total</b></td>")
    for datafile in args.filenames:
        print(f"<td style=\"border: 1px solid\">{BenchmarkResult.success(totals[datafile]).short_format()}</td>")

    print("</tr>")
    print("</table>")
    print("</html>")

if __name__ == "__main__":
    main()
