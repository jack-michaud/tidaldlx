from mutagen.id3 import ID3
from mutagen.mp3 import MP3
from mutagen.mp4 import MP4
from mutagen.flac import FLAC

DEFAULT_TAG_NORMALIZER = {
    "comment": ["©cmt"],
    "title": ["©nam"],
    "artist": ["©ART"],
    "album": ["©alb"],
    "tempo": ["tmpo"],
    "genre": ["@gen"],
}

FLAC_TAG_NORMALIZER = {
    "comment": ["comment"],
    "title": ["title"],
    "artist": ["artist"],
    "album": ["album"],
    "date": ["date"],
    "tempo": ["bpm"],
    "genre": ["genre"],
}


def _get_metadata_container_for_file(file_path: str):
    if file_path.endswith(".m4a"):
        return MP4(file_path)
    elif file_path.endswith(".mp4"):
        return MP4(file_path)
    elif file_path.endswith(".mp3"):
        return MP3(file_path, ID3=ID3)
    elif file_path.endswith(".flac"):
        return FLAC(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")


def _extract_existing_raw_tags(
    file_path: str,
) -> dict[str, str]:
    container = _get_metadata_container_for_file(file_path)
    if isinstance(container, FLAC):
        raw_tags = container
    else:
        raw_tags = container.tags

    return raw_tags  # type: ignore


def _get_tag_for_writing(
    tag: str,
    normalizer: dict[str, list[str]],
) -> str:
    return normalizer.get(tag, [tag])[0]


def read_id3_tags(file_path: str):
    raw_tags = _extract_existing_raw_tags(file_path)

    tags = {}

    if file_path.endswith(".flac"):
        tag_normalizer = FLAC_TAG_NORMALIZER
    else:
        tag_normalizer = DEFAULT_TAG_NORMALIZER

    for key, value in tag_normalizer.items():
        for tag in value:
            try:
                if raw_value := raw_tags.get(tag):
                    tags[key] = raw_value
                    break
            except ValueError as e:
                print(f"Error reading tag {tag}: {e}")

    return tags


def write_tags(
    *,
    file_path: str,
    title: str | None = None,
    artist: str | None = None,
    album: str | None = None,
    comment: str | None = None,
    genre: str | None = None,
) -> None:
    audio = _get_metadata_container_for_file(file_path)
    existing_tags = _extract_existing_raw_tags(file_path)

    if file_path.endswith(".flac"):
        tag_normalizer = FLAC_TAG_NORMALIZER
    else:
        tag_normalizer = DEFAULT_TAG_NORMALIZER

    if title is not None:
        tag = _get_tag_for_writing("title", tag_normalizer)
        existing_tags[tag] = title

    if artist is not None:
        tag = _get_tag_for_writing("artist", tag_normalizer)
        existing_tags[tag] = artist

    if album is not None:
        tag = _get_tag_for_writing("album", tag_normalizer)
        existing_tags[tag] = album

    if comment is not None:
        tag = _get_tag_for_writing("comment", tag_normalizer)
        existing_tags[tag] = comment

    if genre is not None:
        tag = _get_tag_for_writing("genre", tag_normalizer)
        existing_tags[tag] = genre

    if isinstance(audio, FLAC):
        for key, value in existing_tags.items():
            audio[key] = value
        audio.save()
    else:
        audio.tags = existing_tags
        audio.save()
