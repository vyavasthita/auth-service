from dataclasses import dataclass


@dataclass
class BaseException(Exception):
    status_code: int
    message: str

    def __post_init__(self) -> None:
        super().__init__(self.message)

    def __str__(self) -> str:
        return self.message