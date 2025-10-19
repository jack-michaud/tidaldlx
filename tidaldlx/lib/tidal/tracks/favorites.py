from typing import Iterator

from tidalapi.types import ItemOrder, OrderDirection
from tidalapi.user import LoggedInUser
from tidaldlx.lib.tidal.login.session import Session
from tidaldlx.lib.tidal.tracks.track import Track


def fetch_all_favorite_tracks(
    session: Session, limit: int | None = None, reverse: bool = False
) -> Iterator[Track]:
    offset = 0
    batch_limit = 1000

    while True:
        assert session.user is not None
        assert isinstance(session.user, LoggedInUser)

        tracks = session.user.favorites.tracks(
            limit=batch_limit,
            offset=offset,
            order=ItemOrder.Date,
            order_direction=OrderDirection.Ascending
            if reverse
            else OrderDirection.Descending,
        )

        if not tracks:
            break

        for track in tracks:
            yield Track(
                session, media_id=str(track.id) if track.id is not None else None
            )

            if limit is not None:
                limit -= 1
                if limit == 0:
                    break

        offset += batch_limit
