import os
import requests
from pathlib import Path
from typing import Iterator, Protocol

from tidaldlx.lib.files.id3 import write_tags
from tidaldlx.lib.files.track_to_file import (
    TryAgainLaterException,
    get_downloadable_url,
    get_file_name,
)
from tidaldlx.lib.tidal.tracks.track import Track


class Downloader(Protocol):
    def download_tidal_tracks(self, track: Iterator[Track]) -> None: ...


class SingleThreadedDownloader(Downloader):
    def __init__(self, target_directory: str, stop_on_existing: bool = False):
        self.target_directory = Path(target_directory)
        self.session = requests.Session()
        self.stop_on_existing = stop_on_existing

    def download_tidal_tracks(self, tracks: Iterator[Track]) -> None:
        for track in tracks:
            if not self.download_tidal_track(track) and self.stop_on_existing:
                print("Stopping download because an existing file was encountered.")
                break

    def _replace_characters(self, file_name: str) -> str:
        # Replace `/` with `_`
        file_name = file_name.replace("/", "_")
        return file_name

    def download_tidal_track(self, track: Track, attempts: int = 0) -> bool:
        file_name = self._replace_characters(get_file_name(track))

        base_name = os.path.splitext(file_name)[0]

        # If any file with this base name (any extension)
        # exists, we will skip it.
        for f in self.target_directory.iterdir():
            if f.name.startswith(base_name):
                print(f"Skipping {base_name}, already downloaded!")
                self._add_id3_tags(f, track)
                return False

        destination = self.target_directory / file_name

        print(f"Downloading {file_name} to {destination}")

        if destination.exists():
            self._add_id3_tags(destination, track)
            return False

        with open(destination, "wb") as f:
            try:
                url = get_downloadable_url(track)
            except TryAgainLaterException as e:
                print("Rate limited...")
                if attempts < 3:
                    import time

                    time.sleep(1 + 2 * attempts)
                    return self.download_tidal_track(track, attempts + 1)

                raise e

            response = self.session.get(url, stream=True)

            for chunk in response.iter_content(chunk_size=1024):
                print(".", end="")
                f.write(chunk)

        print("Done!")

        self._add_id3_tags(destination, track)
        return True

    def _add_id3_tags(self, file_path: Path, track: Track) -> None:
        try:
            write_tags(
                file_path=file_path.absolute().as_posix(),
                title=track.get_title_tag(),
                artist=track.get_artist_tag(),
                album=track.get_album_tag(),
            )
            print(f"Tags written to {file_path}")
        except Exception as e:
            print(f"Error writing tags to {file_path}: {e}")


def get_downloader(target_directory: str, stop_on_existing: bool = False) -> Downloader:
    return SingleThreadedDownloader(target_directory, stop_on_existing)
