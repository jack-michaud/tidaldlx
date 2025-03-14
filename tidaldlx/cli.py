import argparse
import os
from pathlib import Path

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
    default=str(Path.home() / "Music" / "Tidal"),
)

download_favorites.add_argument(
    "--limit",
    help="Limit the number of tracks to download",
    type=int,
    default=None,
)

download_favorites.add_argument(
    "--reverse",
    help="Download tracks in reverse order (oldest first)",
    action="store_true",
    default=False,
)

read_serato_tags = subcommand.add_parser(
    "read-serato-tags", help="Read Serato tags from files"
)

read_serato_tags.add_argument(
    "files",
    help="Files to read Serato tags from",
    nargs="+",
)

write_serato_tags = subcommand.add_parser(
    "write-serato-tags", help="Write Serato tags to files"
)

write_serato_tags.add_argument(
    "file",
    help="File to write Serato tags to",
)

write_serato_tags.add_argument(
    "--title",
    help="Title of the track",
)

write_serato_tags.add_argument(
    "--artist",
    help="Artist of the track",
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


def main():
    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        return
        
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

        downloader.download_tidal_tracks(fetch_all_favorite_tracks(session, args.limit, args.reverse))

    elif args.command == "read-serato-tags":
        from tidaldlx.lib.files.id3 import read_id3_tags

        for file_path in args.files:
            print(f"File: {file_path}")
            id3_tags = read_id3_tags(file_path)

            if id3_tags is None:
                print(f"Error reading tags from {file_path}")
                continue

            for key, value in id3_tags.items():
                print(f"{key}: {value}")

    elif args.command == "write-serato-tags":
        from tidaldlx.lib.files.id3 import write_tags

        write_tags(
            file_path=args.file,
            title=args.title,
            artist=args.artist,
        )


if __name__ == "__main__":
    main()
