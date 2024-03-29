"""
Bibliothek, die das Carillon als MIDI-Instrument und den Uhrmechanismus
zusammenfasst.
"""

from .carillon import Carillon
from .carillonstriker import CarillonStriker
from .song import Song
from .striker import Striker

__all__ = ['Carillon', 'CarillonStriker', 'Song', 'Striker', ]
