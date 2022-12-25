import mido
from typing import List

from .carillon import Carillon
from .striker import Striker


class CarillonStriker(Striker):
    """
    Erweiterung zum Striker-Modell, das Schläge auf einem Carillon durchführt
    und auch die Möglichkeit zur Wiedergabe einer Melodie bietet.

    Attributes
    ----------
    active : bool
        Kann gesetzt werden, um weitere Schläge zu muten.
    carillon : Carillon
        Carillon, auf dem geschlagen werden soll.

    Methods
    -------
    play(messages)
        Spielt eine Melodie und pausiert währenddessen das Geläut.
    play_active(messages)
        Methode zum Abspielen einer Melodie, die bei `self.active = False`
        abbricht.
    """

    def __init__(self, carillon: Carillon):
        """Erstellt das Objekt und übernimmt ein Carillon."""
        super().__init__()
        self.active = True
        self.carillon = carillon

    def play(self, messages: List[mido.Message]) -> None:
        """Spielt eine Melodie und pausiert währenddessen das Geläut."""
        cache = self.active
        self.active = False
        self.carillon.play(messages)
        self.active = cache

    def play_active(self, messages: List[mido.Message]) -> None:
        """
        Methode zum Abspielen einer Melodie, die bei Deaktivierung des Geläuts
        abbricht.
        """
        for m in messages:
            if not self.active: return
            self.carillon.play([m])
