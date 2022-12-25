from lib.carillon import Carillon, CarillonStriker, Song
from lib.direktorium import TodayDirektorium, Rank, Season

_CustomStriker__sdir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                    'songs')


class CustomStriker(CarillonStriker):

    TRINITATIS = 0x22  # A1SHARP
    MARIA = 0x25       # C2SHARP
    JOSEF = 0x27       # D2SHARP
    APOSTEL = 0x2A     # F2SHARP
    BERNHARD = 0x2C    # G2SHARP
    ENGEL = 0x2E       # A2SHARP

    SONG_LOURDES = Song(os.path.join(_CustomStriker__sdir, 'Lourdes Lied.mid'))
    SONG_MARIANIC = {
        Season.ORDINARY:
            Song(os.path.join(_CustomStriker__sdir, 'Salve Regina.mid')),
        Season.CHRISTMAS:
            Song(os.path.join(_CustomStriker__sdir, 'Alma Redemptoris Mater.mid')),
        Season.LENT:
            Song(os.path.join(_CustomStriker__sdir, 'Ave Regina caelorum.mid')),
        Season.EASTER:
            Song(os.path.join(_CustomStriker__sdir, 'Regina caeli laetare.mid')),
    }
