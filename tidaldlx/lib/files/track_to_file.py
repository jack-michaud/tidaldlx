import tidalapi
from tidaldlx.lib.tidal.tracks.track import Track


def get_file_name(track: Track) -> str:
    artist_names = ", ".join(artist.name for artist in track.artists if artist.name)
    return f"{artist_names} - {track.full_name}.flac"  # TODO: when configuring quality, this may become flac.


class TryAgainLaterException(Exception):
    pass


def get_downloadable_url(track: Track) -> str:
    try:
        return track.get_url()
    except tidalapi.exceptions.TooManyRequests as e:
        raise TryAgainLaterException from e
