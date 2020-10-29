"""
Bibliothek, die das Carillon als MIDI-Instrument und den Uhrmechanismus
zusammenfasst.
"""

from .carillon import Carillon
from .quarterclock import QuarterClock, QuarterClockObserver

__all__ = ['Carillon', 'QuarterClock', 'QuarterClockObserver', ]
