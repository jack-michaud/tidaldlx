# TidalDLX

A Tidal Downloader for one-way syncing your liked songs to a folder.

## Installation

### Using pipx (recommended)

[pipx](https://pypa.github.io/pipx/) allows you to install and run Python applications in isolated environments:

```bash
# Install pipx if you don't have it
python -m pip install --user pipx
python -m pipx ensurepath

# Install tidaldlx
pipx install git+https://github.com/jack-michaud/tidaldlx.git
```

### Using pip

You can also install with pip directly:

```bash
pip install git+https://github.com/jack-michaud/tidaldlx.git
```

### From source

```bash
# Clone the repository
git clone https://github.com/jack-michaud/tidaldlx.git
cd tidaldlx

# Install in development mode
pip install -e .
```

## Usage

First, log in to Tidal:

```bash
tidaldlx login
```

Then download your favorite tracks:

```bash
tidaldlx download-favorites --output-dir /path/to/download/directory
```

### Options

- `--output-dir`: Directory to download tracks to (default: ~/Music/Tidal)
- `--limit`: Limit the number of tracks to download
- `--reverse`: Download tracks in reverse order (oldest first)
- `--stop-on-existing`: Stop downloading when an already downloaded file is encountered

### Serato Tags

TidalDLX also includes utilities for working with Serato tags:

Read tags from files:
```bash
tidaldlx read-serato-tags file1.flac file2.flac
```

Write tags to a file:
```bash
tidaldlx write-serato-tags file.flac --title "Track Title" --artist "Artist Name"
```