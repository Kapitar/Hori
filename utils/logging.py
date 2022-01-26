import time
import sys
from functools import cache
from enum import IntEnum


class Ansi(IntEnum):
    BLACK   = 30
    RED     = 31
    GREEN   = 32
    YELLOW  = 33
    BLUE    = 34
    MAGENTA = 35
    CYAN    = 36
    WHITE   = 37

    GRAY     = 90
    LRED     = 91
    LGREEN   = 92
    LYELLOW  = 93
    LBLUE    = 94
    LMAGENTA = 95
    LCYAN    = 96
    LWHITE   = 97

    RESET = 0

    @cache
    def __repr__(self) -> str: return f'\x1b[{self.value}m'


def format_time() -> str:
    return time.strftime("%Y-%d-%m %H:%M:%S", time.localtime())


def log(message: str, log_type: str, color: Ansi = Ansi.WHITE) -> None:
    sys.stdout.write(
        f"\033[37m{Ansi.GRAY!r}\033[49m[{format_time()} - {log_type}]"
        f"\033[37m{color!r}\033[49m {message}"
        "\033[39m\n"
    )


def debug(message: str) -> None: log(message, "DEBUG", Ansi.LGREEN)
def info(message: str) -> None: log(message, "INFO", Ansi.LBLUE)
def error(message: str) -> None: log(message, "ERROR", Ansi.LRED)
def warning(message: str) -> None: log(message, "WARNING", Ansi.LYELLOW)