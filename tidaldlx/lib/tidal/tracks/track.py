from tidalapi import Track as _Track


class Track(_Track):
    def get_artist_tag(self) -> str | None:
        return ", ".join([a.name for a in self.artists if a.name is not None])

    def get_album_tag(self) -> str | None:
        return self.album.name

    def get_title_tag(self) -> str | None:
        return self.name
