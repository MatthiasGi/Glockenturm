from dataclasses import (dataclass, field, InitVar)
from glob import glob
import mido
import os
import re
from typing import List


@dataclass
class Song:
    """
    Wrapper für eine MIDI-Datei, die ein Lied für das Carillon abbildet.

    Attributes
    ----------
    title : str
        Titel des Liedes.
    number : str
        Gotteslobnummer.
    tempo : int
        Wiedergabetempo.
    transpose : int
        Anzahl der Halbtöne, um die transponiert werden soll.
    file : mido.MidiFile
        Eingelesene Datei.
    messages : List[mido.Message]
        Liste an Nachrichten, die in der Datei enthalten sind (passend
        transponiert und mit richtigem Tempo ausgestattet).

    Class methods
    -------------
    from_file(filepath, number, title) : Song
        Versucht ein Objekt aus einer MIDI-Datei zu lesen.
    from_number(basepath, number, title) : Song
        Versucht ein Objekt aus einer MIDI-Datei zu lesen, die anhand einer
        Gotteslobnummer identifiziert wird.
    from_title(basepath, title) : Song
        Versucht ein Objekt aus einer MIDI-Datei zu lesen, die anhand eines
        Titels identifiziert wird.
    """

    filepath: InitVar[str]
    title: str
    number: str = None
    tempo: int = field(init=False)
    transpose: int = field(default=0, init=False)
    file: mido.MidiFile = field(init=False)

    def __post_init__(self, filepath: str) -> None:
        """
        Schließt die Initialisierung der Datei ab, indem die MIDI-Datei in das
        `file`-Objekt eingelesen wird.

        Parameters
        ----------
        filepath : str
            Pfad zur MIDI-Datei, der dem Konstruktor mit übergeben wurde.
        """
        self.file = mido.MidiFile(filepath)
        for msg in self.file.tracks[0]:
            if msg.type != 'set_tempo': continue
            self.tempo = msg.tempo
            break

    @property
    def messages(self) -> List[mido.Message]:
        """
        MIDI-Nachrichten aus der Datei, Tempo und Transponierung angewendet.
        """
        messages = []
        for msg in self.file.tracks[0]:
            if msg.type not in ('note_on', 'note_off'): continue
            time = mido.tick2second(msg.time, self.file.ticks_per_beat,
                                    self.tempo)
            note = msg.note + self.transpose
            messages.append(msg.copy(time=time, note=note))
        return messages

    @classmethod
    def from_file(
        cls, filepath: str, number: str = None, title: str = None
    ) -> 'Song':
        """
        Versucht, ein Song-Objekt aus einer Datei zu erstellen.

        Parameters
        ----------
        filepath : str
            Pfad zur MIDI-Datei, die eingelesen werden soll.
        number : str (optional)
            Gotteslobnummer, falls nicht angegeben, wird sie aus dem Dateinamen
            gelesen.
        title : str (optional)
            Titel, falls nicht angegeben, wird er aus dem Dateinamen gelesen.

        Returns
        -------
        Die eingelesene MIDI-Datei, gekapselt als Song-Objekt.

        Raises
        ------
        FileNotFoundError
            Falls die angegebene Datei nicht gefunden werden konnte.
        """
        if not os.path.exists(filepath):
            raise FileNotFoundError(f'Datei {filepath} wurde nicht gefunden!')
        name = os.path.splitext(os.path.basename(filepath))[0]

        if number is None:
            candidate = name.split(' ', 1)
            if re.fullmatch(r'\d{1,3}(,\d)?', candidate[0]):
                number, name = candidate
        elif name.startswith(f'{number} '): name = name[len(number) + 1:]

        if title is None: title = name
        return Song(title=title, filepath=filepath, number=number)

    @classmethod
    def from_number(
        cls, basepath: str, number: str, title: str = None
    ) -> 'Song':
        """
        Versucht ein Song-Objekt aus einer Datei einzulesen, die anhand der
        Gotteslobnummer im Titel identifiziert wird.

        Parameters
        ----------
        basepath : str
            Pfad, in dem gesucht werden soll.
        number : str
            Gotteslobnummer, die gesucht werden soll.
        title : str (optional)
            Titel des Liedes, wird ansonsten aus dem Dateinamen gelesen.

        Returns
        -------
        Die eingelesene MIDI-Datei als gekapseltes Song-Objekt.

        Raises
        ------
        FileNotFoundError
            Falls keine Datei mit der entsprechenden Gotteslobnummer gefunden
            werden konnte.
        """
        path = os.path.join(basepath, '**', f'{number}*.mid')
        songs = glob(path, recursive=True)
        if len(songs) < 1:
            raise FileNotFoundError(f'{number} in {basepath} nicht gefunden!')
        return Song.from_file(songs[0])

    @classmethod
    def from_title(cls, basepath: str, title: str) -> 'Song':
        """
        Versucht ein Song-Objekt aus einer Datei einzulesen, die anhand eines
        Titels identifiziert wird.

        Parameters
        ----------
        basepath : str
            Pfad, in dem gesucht werden soll.
        title : str
            Titel, nach dem gesucht werden soll.

        Returns
        -------
        Die eingelesene MIDI-Datei als gekapseltes Song-Objekt.

        Raises
        ------
        FileNotFoundError
            Wenn keine Datei mit dem entsprechenden Titel gefunden werden
            konnte.
        """
        path = os.path.join(basepath, '**', f'{title}.mid')
        songs = glob(path, recursive=True)
        if len(songs) < 1:
            raise FileNotFoundError(f'{title} in {basepath} nicht gefunden!')
        return Song.from_file(songs[0])
