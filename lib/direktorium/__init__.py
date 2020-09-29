"""
Das Direktorium hält eine aktuelle Liste über tagesaktuelle Feste bereit. Es
fragt dazu die API https://www.eucharistiefeier.de/lk/ ab und cached Ergebnisse
optional.
"""

from .color import Color
from .direktorium import Direktorium
from .event import Event
from .rank import Rank

__all__ = ['Color', 'Direktorium', 'Rank', 'Event', ]
