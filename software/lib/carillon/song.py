import mido
from typing import List


class Song:
    """
    Wrapper für eine MIDI-Datei, die ein Lied für das Carillon abbildet.

    Attributes
    ----------
    file : mido.MidiFile
        Eingelesene Datei.
    tempo : int
        Widergabetempo.
    transpose : int
        Anzahl der Halbtöne, um die transponiert werden soll.
    messages : List[mido.Message]
        Liste an Nachrichten, die in der Datei enthalten sind (passend
        transponiert und mit richtigem Tempo ausgestattet).
    """

    def __init__(self, path: str):
        """
        Erstellt den Song, indem er ihn aus der Datei liest und Attribute
        vorbelegt.

        Parameters
        ----------
        path : str
            Pfad zur einzulesenden MIDI-Datei.
        """
        self.file = mido.MidiFile(path)
        self.transpose = 0

        g = (m.tempo for m in self.file.tracks[0] if m.type == 'set_tempo')
        self.tempo = next(g, 500_000)

    @property
    def messages(self) -> List[mido.Message]:
        """
        MIDI-Nachrichten aus der Datei, Tempo und Transponierung angewendet.
        """
        messages = [m.copy() for m in self.file.tracks[0]
                    if m.type in ('note_on', 'note_off')]
        tpb = self.file.ticks_per_beat
        for m in messages:
            m.time = mido.tick2second(m.time, tpb, self.tempo)
            m.note += self.transpose
        return messages
