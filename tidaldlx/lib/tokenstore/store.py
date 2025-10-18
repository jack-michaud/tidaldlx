from datetime import datetime
import json

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Token:
    token_type: str
    access_token: str
    refresh_token: str
    expiry_time: datetime


class NotFoundError(Exception):
    pass


class TokenStore(Protocol):
    def store(self, token: Token) -> None: ...

    def retrieve(self) -> Token: ...

    def clear(self) -> None: ...


class RawFileTokenStore(TokenStore):
    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def store(self, token: Token) -> None:
        with open(self.file_path, "w") as file:
            json.dump(
                {
                    "token_type": token.token_type,
                    "access_token": token.access_token,
                    "refresh_token": token.refresh_token,
                    "expiry_time": token.expiry_time.isoformat(),
                },
                file,
            )

    def retrieve(self) -> Token:
        try:
            with open(self.file_path, "r") as file:
                token_data = json.load(file)
                token_data["expiry_time"] = datetime.fromisoformat(
                    token_data["expiry_time"]
                )
                return Token(**token_data)
        except FileNotFoundError:
            raise NotFoundError("Token file not found")

    def clear(self) -> None:
        """Delete the cached token file"""
        try:
            import os
            os.remove(self.file_path)
        except FileNotFoundError:
            pass


def get_token_store() -> TokenStore:
    return RawFileTokenStore("token.json")
