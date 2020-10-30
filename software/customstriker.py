from datetime import date, timedelta
import os
import time

from lib.carillon import Carillon, Striker
from lib.direktorium import TodayDirektorium, Rank, Season
from lib.songs import Song

_CustomStriker__sdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'songs')


class CustomStriker(Striker):
    """
    Klasse, die den Striker der Bibliothek erweitert und ein eigenes
    Stundengeläut möglichst schlicht zur Verfügung stellt.

    Constants
    ---------
    TRINITATIS : int
    MARIA : int
    JOSEF : int
    APOSTEL : int
    BERNHARD : int
    ENGEL : int
    SONG_LOURDES : Song
        Lourdes-Lied, das Mittags gespielt wird.
    SONG_MARIANIC : dict
        Dictionary, das jeder Season einen Song (marianische Antiphon)
        zuordnet.

    Attributes
    ----------
    carillon : Carillon
        Carillon, auf dem geschlagen werden soll.
    direktorium : TodayDirektorium
        Ein Direktorium, das Infos für den heutigen Tag cacht.

    Methods
    -------
    strike(hours, quarters)
        Schlägt die Stunden und Viertelstunden an.
    tell(hours, quarters)
        Reagiert auf das automatische Triggern.
    """

    TRINITATIS = 0x22  # A1SHARP
    MARIA = 0x25       # C2SHARP
    JOSEF = 0x27       # D2SHARP
    APOSTEL = 0x2A     # F2SHARP
    BERNHARD = 0x2C    # G2SHARP
    ENGEL = 0x2E       # A2SHARP

    SONG_LOURDES = Song.from_file(os.path.join(__sdir, 'Lourdes Lied.mid'))
    SONG_MARIANIC = {
        Season.ORDINARY:
            Song.from_file(os.path.join(__sdir, 'Salve Regina.mid')),
        Season.CHRISTMAS:
            Song.from_file(os.path.join(__sdir, 'Alma Redemptoris Mater.mid')),
        Season.LENT:
            Song.from_file(os.path.join(__sdir, 'Ave Regina caelorum.mid')),
        Season.EASTER:
            Song.from_file(os.path.join(__sdir, 'Regina caeli laetare.mid')),
    }

    def __init__(self, carillon: Carillon, direktorium: TodayDirektorium):
        """Erstellt das Objekt und übernimmt Carillon und Direktorium."""
        super().__init__()
        self.carillon = carillon
        self.direktorium = direktorium

    def strike(self, hours: int, quarters: int) -> None:
        """Schlägt die spezifizierte Zahl an (Viertel-)Stunden an."""

        # Nachtschaltung
        if hours > 21 or (hours == 21 and quarters > 2): return
        if hours < 8: return

        # Schweigen an Karfreitag und -samstag
        easter = self.direktorium.easter()
        if date.today() == easter - timedelta(days=1): return
        if date.today() == easter - timedelta(days=2): return

        # Mittagsgeläut
        if hours == 12 and quarters == 0:
            self.tell(12, 4)
            return self.carillon.play(CustomStriker.SONG_LOURDES.messages)

        # Abendgeläut
        if hours == 21 and quarters == 2:
            self.tell(21, 2)
            antiphon = CustomStriker.SONG_MARIANIC[self.direktorium.season()]
            return self.carillon.play(antiphon.messages)

        # Sonstiges, „normales“ Geläut
        hours %= 12
        if hours == 0: hours = 12
        if quarters == 0:
            self.tell(hours, 4)
        else:
            self.tell(0, quarters)

    def tell(self, hours: int, quarters: int) -> None:
        """Reagiert auf den Viertelstundentrigger."""
        for i in range(quarters):
            events = self.direktorium.get()
            if events and events[0].rank >= Rank.GEBOTEN:
                self.carillon.hit(CustomStriker.ENGEL)
                time.sleep(0.5)
                self.carillon.hit(CustomStriker.BERNHARD)
                time.sleep(0.5)
                self.carillon.hit(CustomStriker.APOSTEL)
                time.sleep(1.5)
            else:
                self.carillon.hit(CustomStriker.ENGEL)
                time.sleep(2)

        for i in range(hours):
            self.carillon.hit(CustomStriker.TRINITATIS)
            time.sleep(2.5)
