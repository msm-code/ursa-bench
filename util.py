from typing import TYPE_CHECKING, Dict, TypedDict, Optional
if TYPE_CHECKING:
    from typing import Self
else:
    Self = None

class Statistics(TypedDict):
    and_count: int
    and_milliseconds: int
    minof_count: int
    minof_milliseconds: int
    or_count: int
    or_milliseconds: int
    read_count: int
    read_milliseconds: int
    uniq_read_count: Optional[int]
    uniq_read_milliseconds: Optional[int]
    file_count: int


class BenchmarkResult:
    def __init__(self, status: str, msg: Optional[str], stats: Optional[Statistics]):
        self.status = status
        self.message = msg
        self.stats = stats

    @classmethod
    def success(cls, stats: Statistics) -> Self:
        return cls("success", None, stats)

    @classmethod
    def empty(cls) -> Self:
        return cls("empty", None, None)

    @classmethod
    def degenerate(cls) -> Self:
        return cls("degenerate", None, None)

    @classmethod
    def yaramod_error(cls, message: str) -> Self:
        return cls("yaramod_error", message, None)

    @classmethod
    def ursadb_error(cls, message: str) -> Self:
        return cls("ursadb_error", message, None)

    def short_format_alt(self) -> str:
        if self.status == "success":
            assert self.stats is not None
            return f"{self.stats['file_count']} ({self.stats['and_milliseconds']  + self.stats['or_milliseconds'] + self.stats['minof_milliseconds'] + self.stats['read_milliseconds']}ms)"
        else:
            return self.status

    def short_format(self) -> str:
        if self.status == "success":
            assert self.stats is not None
            return (
                f"files: {self.stats['file_count']}<br>"
                f"ands: {self.stats['and_count']} ({self.stats['and_milliseconds']}ms)<br>"
                f"ors: {self.stats['or_count']} ({self.stats['or_milliseconds']}ms)<br>"
                f"minofs: {self.stats['minof_count']} ({self.stats['minof_milliseconds']}ms)<br>"
                f"reads: {self.stats['read_count']} ({self.stats['read_milliseconds']}ms)"
            )
        else:
            return self.status
