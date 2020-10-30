from glob import glob
import os
from typing import List

from .song import Song


class Library:
    """
    Liest alle MIDI-Dateien als Songs ein und stellt diese zur Verfügung.

    Attribtues
    ----------
    songs : List[Song]
        Liste aller eingelesenen Songs.

    Methods
    -------
    search_number(number) : Song
        Sucht ein Lied anhand der Gotteslobnummer.
    search_title(title) : List[Song]
        Gibt alle Lieder zurück, die `title` im Titel tragen.
    """

    def __init__(self, path: str):
        """
        Erstellt die Bibliothek und liest alle Songs aus dem übergebenen
        Verzeichnis ein.

        Parameters
        ----------
        path : str
            Pfad des Verzeichnisses, das eingelesen werden soll.
        """
        path = os.path.join(path, '**', f'*.mid')
        songs = glob(path, recursive=True)
        self.songs = [Song.from_file(s) for s in songs]

    def search_number(self, number: str) -> Song:
        """
        Ermittelt das Lied mit der übergebenen Gotteslobnummer.

        Parameters
        ----------
        number : str
            Gotteslobnummer, die gesucht werden soll.

        Returns
        -------
        Lied, das die gegebene Gotteslobnummer trägt.
        """
        for s in Library.songs():
            if str(number) == s.number: return s

    def search_title(self, title: str) -> List[Song]:
        """
        Ermittelt alle Lieder, die den übergebenen String als Bestandteil im
        Titel tragen.

        Parameters
        ----------
        title : str
            Zu suchender Titelbestandteil. Um die Suche zu erleichtern, wird
            Groß- und Kleinschreibung nicht berücksichtigt.

        Returns
        -------
        Liste aller Songs, die den gegebenen Bestandteil im Titel tragen.
        """
        title = title.lower()
        found = []
        for s in Library.songs():
            if title in s.title.lower(): found.append(s)
        return found
