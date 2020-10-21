import dataclasses

from typing import Dict

from .cast_dict_to import cast_dict_to


@dataclasses.dataclass(frozen=True)
class LoggingConfig:
    log_level: str = "INFO"
    log_filename: str = "log/debug.log"
    log_stdout: bool = False

    @classmethod
    def from_dict(cls, d: Dict) -> "LoggingConfig":
        return cast_dict_to(d, cls)
