from networkx.classes.multidigraph import MultiDiGraph
from enum import Enum


class IncorrectHash(Exception):
    pass


class DownloadStatus(Enum):

    SUCCESS = 1
    ALREADY_EXISTS = 2
