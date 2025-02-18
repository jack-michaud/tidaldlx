from typing import Iterator
from tidaldlx.lib.tidal.login.session import Session
from tidaldlx.lib.tidal.tracks.track import Track


def fetch_all_favorite_tracks(
    session: Session, limit: int | None = None
) -> Iterator[Track]:
    offset = 0
    batch_limit = 1000
    while True:
        tracks = session.user.favorites.tracks(
            limit=batch_limit, offset=offset, order="DATE"
        )

        if not tracks:
            break

        for track in tracks:
            yield track

            if limit is not None:
                limit -= 1
                if limit == 0:
                    break

        offset += batch_limit
