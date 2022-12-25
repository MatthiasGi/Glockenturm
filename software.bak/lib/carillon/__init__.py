"""
Bibliothek, die das Carillon als MIDI-Instrument und den Uhrmechanismus
zusammenfasst.
"""

from .carillon import Carillon
from .striker import Striker

__all__ = ['Carillon', 'Striker', ]
