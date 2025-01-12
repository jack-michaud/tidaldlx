import argparse

from tidaldlx.lib.tokenstore.store import TokenStore, NotFoundError, get_token_store
from tidaldlx.lib.tidal.config import get_tidal_config
from tidaldlx.lib.tidal.login.session import get_tidal_session
from tidaldlx.lib.ui.notify import get_notify

parser = argparse.ArgumentParser(description="tidaldlx")

subcommand = parser.add_subparsers(dest="command")

login = subcommand.add_parser("login", help="Log in to Tidal")


def get_session(token_store: TokenStore):
    session = get_tidal_session(get_tidal_config())

    if not session.check_login():
        try:
            token = token_store.retrieve()
            session.load_token(token)
        except NotFoundError:
            pass

    return session


if __name__ == "__main__":
    args = parser.parse_args()
    if args.command == "login":
        from tidaldlx.lib.tidal.login.prompt import PromptForLogin

        token_store = get_token_store()
        notify = get_notify()
        session = get_session(token_store)
        prompt = PromptForLogin(notify)

        if prompt.needs_login(session):
            logged_in = prompt.prompt_for_login(session)
            if logged_in:
                token_store.store(session.get_token())
        else:
            print("Already logged in")
    else:
        print("Unknown command")
