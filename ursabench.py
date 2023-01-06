import yaramod
import json
import argparse
from yaraparse import parse_yara, combine_rules
from pathlib import Path
from ursadb import UrsaDb
from util import BenchmarkResult, Statistics


def get_statistics(data) -> Statistics:
    return {
        "and_count": data["counters"]["and"]["count"],
        "and_milliseconds": data["counters"]["and"]["milliseconds"],
        "minof_count": data["counters"]["minof"]["count"],
        "minof_milliseconds": data["counters"]["minof"]["milliseconds"],
        "or_count": data["counters"]["or"]["count"],
        "or_milliseconds": data["counters"]["or"]["milliseconds"],
        "read_count": data["counters"]["read"]["count"],
        "read_milliseconds": data["counters"]["read"]["milliseconds"],
        "uniq_read_count": data["counters"]["uniq_read"]["count"] if "uniq_read" in data["counters"] else None,
        "uniq_read_milliseconds": data["counters"]["uniq_read"]["milliseconds"] if "uniq_read" in data["counters"] else None,
        "file_count": len(data["result"]["files"])
    }


def measure(file: Path) -> BenchmarkResult:
    text = file.read_text()
    try:
        rules = parse_yara(text)
    except yaramod.ParserError as e:
        return BenchmarkResult.yaramod_error(repr(e))

    if not rules:
        return BenchmarkResult.empty()

    final_query = combine_rules(rules)
    if final_query.is_degenerate:
        return BenchmarkResult.degenerate()

    query = final_query.query

    db = UrsaDb("tcp://localhost:9281")

    out = db.execute_command(f"select {query};")

    if 'error' in out:
        return BenchmarkResult.ursadb_error(out["error"])

    stats = get_statistics(out)
    return BenchmarkResult.success(stats)

def measure_and_print(file: Path) -> None:
    result = measure(file)
    out_dict = {
        "filename": file.name,
        "status": result.status,
        "message": result.message,
        "stats": result.stats,
    }
    print(json.dumps(out_dict))


def main() -> None:
    parser = argparse.ArgumentParser(description="UrsaDB benchmark suite.")
    parser.add_argument("filenames", help="yar file to measure", nargs="+")
    parser.add_argument("--url", "-u", help="ursadb api url", nargs="?", default="tcp://localhost:9281")
    args = parser.parse_args()

    for filename in args.filenames:
        measure_and_print(Path(filename))

if __name__ == "__main__":
    main()
