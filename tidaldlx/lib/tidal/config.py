import tidalapi

from tidalapi import Config as Config


def get_tidal_config() -> Config:
    return tidalapi.Config(
        quality=tidalapi.Quality.high_lossless,
        alac=False,  # Only audio
    )


__all__ = ["get_tidal_config", "Config"]
