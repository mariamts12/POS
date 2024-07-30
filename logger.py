from dataclasses import dataclass, field
from typing import Protocol


class LoggerProtocol(Protocol):
    def new_entry(self, data: list[list[object]], headers: list[object]) -> None:
        pass

    def compute_max_lengths(self) -> None:
        pass

    def print_table(self, data: list[list[object]], headers: list[object]) -> None:
        pass

    def print_row(self, row: list[object], fill_char: str) -> None:
        pass


@dataclass
class Logger(LoggerProtocol):
    data: list[list[object]] = field(default_factory=list)
    headers: list[object] = field(default_factory=list)
    max_lengths: list[int] = field(default_factory=list)
    rows: int = 0
    columns: int = 0

    def new_entry(self, data: list[list[object]], headers: list[object]) -> None:
        self.data = data
        self.headers = headers
        self.rows = len(data)
        self.columns = len(data[0])

    def compute_max_lengths(self) -> None:
        rows = len(self.data)
        columns = len(self.data[0])
        max_lengths: list[int] = []

        for col in range(columns):
            current = 0
            for row in range(rows):
                current = max(current, len(str(self.data[row][col])))
            max_lengths.append(max(current, len(str(self.headers[col]))))
        self.max_lengths = max_lengths

    def print_table(self, data: list[list[object]], headers: list[object]) -> None:
        self.new_entry(data, headers)
        self.compute_max_lengths()
        self.print_row(headers, " ")
        self.print_row([""] * self.columns, "-")

        for row in range(self.rows):
            self.print_row(data[row], " ")
        print()

    def print_row(self, row: list[object], fill_char: str) -> None:
        result = "| "
        for x in range(len(row)):
            result += str(row[x]).ljust(self.max_lengths[x], fill_char) + " | "
        print(result)
