from tidalapi import Session as _Session

from tidaldlx.lib.tidal.config import Config
from tidaldlx.lib.tokenstore.store import Token


class NotLoggedInError(Exception):
    pass


class Session(_Session):
    def get_token(self) -> Token:
        if not self.check_login():
            raise NotLoggedInError("Not logged in")

        return Token(
            token_type=self.token_type,
            access_token=self.access_token,
            refresh_token=self.refresh_token,
            expiry_time=self.expiry_time,
        )

    def load_token(self, token: Token) -> None:
        self.load_oauth_session(
            token_type=token.token_type,
            access_token=token.access_token,
            refresh_token=token.refresh_token,
            expiry_time=token.expiry_time,
        )


def get_tidal_session(config: Config) -> Session:
    return Session(config)


__all__ = ["get_tidal_session", "Session"]
