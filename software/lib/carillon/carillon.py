import mido
import mido.backends.rtmidi
import time
from typing import List
import warnings


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
    play(messages)
        Spielt eine Melodie auf dem Carillon.
    """

    def __init__(self, port: mido.backends.rtmidi.Output = None):
        """
        Erzeugt das Carillon und belegt es mit einem MIDI-Port vor.

        Paramteres
        ----------
        port : mido.backends.rtmidi.Output (optional)
            MIDI-Port, der genutzt werden soll. Sofern keiner übergeben wird,
            wird ein Standardport geöffnet.
        """
        self.port = mido.open_output() if port is None else port

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
            warnings.warn(f'Note {note} nicht verfügbar.')
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
