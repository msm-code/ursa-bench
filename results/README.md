# Benchmark results

All tests done on the same machine.

Result name format: `{version}_{disk}_{indexes}.txt`

For example `0_init_hdd_all.txt` means:
    - The version tested is `0_init`
    - Database was stored on `hdd`
    - `all` means that all indexes were tested.

List of tested versions:
    - `0_init` - initial version
    - `1_queryplan` - PR fix/performance1-queryplan

List of tested storage options:
    - `hdd`
    - `ssd`

List of tested database configurations:
    - `all`
    - `nohash4`



### Benchmark files:




queryplan_log_without_hash4_hdd.txt
