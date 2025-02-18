import os
import requests
from pathlib import Path
from typing import Iterator, Protocol

from tidaldlx.lib.files.track_to_file import (
    TryAgainLaterException,
    get_downloadable_url,
    get_file_name,
)
from tidaldlx.lib.tidal.tracks.track import Track


class Downloader(Protocol):
    def download_tidal_tracks(self, track: Iterator[Track]) -> None: ...


class SingleThreadedDownloader(Downloader):
    def __init__(self, target_directory: str):
        self.target_directory = Path(target_directory)
        self.session = requests.Session()

    def download_tidal_tracks(self, tracks: Iterator[Track]) -> None:
        for track in tracks:
            self.download_tidal_track(track)

    def download_tidal_track(self, track: Track, attempts: int = 0) -> None:
        file_name = Path(get_file_name(track))

        base_name = os.path.splitext(file_name)[0]

        # If any file with this base name (any extension)
        # exists, we will skip it.
        if any(
            f.name.startswith(base_name)
            for f in self.target_directory.glob(f"{base_name}*")
        ):
            print(f"Skipping {base_name}, already downloaded!")
            return

        destination = self.target_directory / file_name

        print(f"Downloading {file_name} to {destination}")

        if destination.exists():
            return

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


def get_downloader(target_directory: str) -> Downloader:
    return SingleThreadedDownloader(target_directory)
