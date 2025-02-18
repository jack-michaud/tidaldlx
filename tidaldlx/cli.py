import argparse

from tidaldlx.lib.files.downloader import get_downloader
from tidaldlx.lib.tokenstore.store import TokenStore, NotFoundError, get_token_store
from tidaldlx.lib.tidal.config import get_tidal_config
from tidaldlx.lib.tidal.login.session import get_tidal_session
from tidaldlx.lib.ui.notify import get_notify

parser = argparse.ArgumentParser(description="tidaldlx")

subcommand = parser.add_subparsers(dest="command")

login = subcommand.add_parser("login", help="Log in to Tidal")

download_favorites = subcommand.add_parser(
    "download-favorites", help="List favorite tracks"
)

download_favorites.add_argument(
    "--output-dir",
    help="Directory to download tracks to",
    default="/Users/jack/Music/DjDownloads/Tidal/",
)


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
    elif args.command == "download-favorites":
        from tidaldlx.lib.tidal.tracks.favorites import fetch_all_favorite_tracks

        token_store = get_token_store()
        session = get_session(token_store)

        downloader = get_downloader(args.output_dir)

        downloader.download_tidal_tracks(fetch_all_favorite_tracks(session))
