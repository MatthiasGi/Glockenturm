from dataclasses import dataclass
import mido
import time
from typing import List
import warnings


@dataclass
class Carillon:
    """
    Klasse, die die Kommunikation zu GrandOrgue über MIDI-Messages abstrahiert
    zur Verfügung stellt.

    Attributes
    ----------
    port : mido.backends.rtmidi.Output
        MIDI-Port, an den die Nachrichten gesendet werden.

    Methods
    -------
    hit(note)
        Schlägt eine Glocke an.
    play(*messages)
        Spielt eine Melodie auf dem Carillon.
    """

    port: mido.backends.rtmidi.Output = mido.open_output()

    def hit(self, note: int) -> None:
        """
        Schlägt eine einzelne Glocke an, sofern diese im Carillon existiert
        (andernfalls wird eine Warnung ausgegeben).

        Parameters
        ----------
        note : int
            MIDI-Notenwert der anzuschlagenden Glocke.
        """
        if note < 34 or note > 89:
            warnings.warn(f'Note {note} nicht durch das Carillon abgebildet!')
        else:
            self.port.send(mido.Message('note_on', note=note))
            self.port.send(mido.Message('note_off', note=note))

    def play(self, messages: List[mido.Message]) -> None:
        """
        Spielt eine übergebene Melodie auf dem Carillon.

        Parameters
        ----------
        messages : List[mido.Message]
            MIDI-Nachrichten, die die Melodie kodieren.
        """
        for msg in messages:
            time.sleep(msg.time)
            if msg.type == 'note_on' and msg.velocity != 0: self.hit(msg.note)
