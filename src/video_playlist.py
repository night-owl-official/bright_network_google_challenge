"""A video playlist class."""

from typing import Sequence

from .video import Video

class Playlist:
    """A class used to represent a Playlist."""

    def __init__(self, name: str, videos: Sequence[Video]):
        self._name = name
        self._videos = videos


    def __eq__(self, other):
        return self._name == other._name
    

    @property
    def name(self) -> str:
        return self._name

    @property
    def videos(self) -> Sequence[Video]:
        return self._videos
