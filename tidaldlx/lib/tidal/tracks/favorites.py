from typing import Iterator
from tidaldlx.lib.tidal.login.session import Session
from tidaldlx.lib.tidal.tracks.track import Track


def fetch_all_favorite_tracks(session: Session) -> Iterator[Track]:
    offset = 0
    limit = 1000
    while True:
        tracks = session.user.favorites.tracks(limit=limit, offset=offset, order="DATE")

        if not tracks:
            break

        for track in tracks:
            yield track

        offset += limit
