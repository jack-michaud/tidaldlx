from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TYER, COMM, error
from mutagen.mp3 import MP3
from tidaldlx_contrib.serato_tags.database_v2 import parse
from mutagen.mp4 import MP4


def add_id3_tags(
    file_path: str,
    title: str,
    artist: str,
    album: str,
    track_number: int,
    year: str,
    comment: str,
):
    try:
        audio = MP3(file_path, ID3=ID3)
    except error as e:
        print(f"Error reading file {file_path}: {e}")
        return

    if audio.tags is None:
        audio.add_tags()

    # Add or update tags
    audio.tags.add(TIT2(encoding=3, text=title))
    audio.tags.add(TPE1(encoding=3, text=[artist]))
    audio.tags.add(TALB(encoding=3, text=album))
    audio.tags.add(TRCK(encoding=3, text=str(track_number)))
    audio.tags.add(TYER(encoding=3, text=year))
    audio.tags.add(COMM(encoding=3, lang="eng", desc="desc", text=[comment]))

    # Save the file
    try:
        audio.save()
    except error as e:
        print(f"Error saving tags to {file_path}: {e}")


def read_id3_tags(file_path: str):
    try:
        if file_path.endswith(".mp4"):
            audio = MP4(file_path)
        elif file_path.endswith(".mp3"):
            audio = MP3(file_path, ID3=ID3)
        else:
            raise ValueError(f"Unsupported file type: {file_path}")
    except error as e:
        print(f"Error reading file {file_path}: {e}")
        return

    return audio.tags


def read_serato_tags(file_path: str):
    with open(file_path, "rb") as fp:
        return dict(parse(fp))


# Example usage:
# add_id3_tags('path/to/file.mp3', 'Song Title', 'Artist Name', 'Album Name', 1, '2023', 'This is a comment')
# tags = read_id3_tags('path/to/file.mp3')
# print(tags)
