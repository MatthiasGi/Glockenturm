from dataclasses import dataclass
from datetime import date
import json
import os
import requests
from typing import List

from .event import Event


@dataclass
class Direktorium:
    """
    Stellt das Direktorium mit einem Cache und einem Regionalkalender zur
    Verfügung.

    Attributes
    ----------
    kalender : str
        Kalenderbezeichnung nach
        https://www.eucharistiefeier.de/lk/api-abfrage.php.
    cache_dir : str
        Verzeichnis, in dem Ergebnisse zwischengespeichert werden sollen.
    """

    kalender: str = 'deutschland'
    cache_dir: str = None

    def get(self, d: date) -> List[Event]:
        """Gibt eine List von Events für ein angegebenes Datum zurück."""
        r = self.request_cache(d)
        entries = [Event.parse(e) for e in r.json()['Zelebrationen'].values()]
        entries.sort(key=lambda e: e.importance)
        return entries

    def request_api(
        self, year: int, month: int = None, day: int = None
    ) -> requests.models.Response:
        """
        Fragt die API online direkt ab, optional können Monat und Tag angegeben
        werden.
        """
        url = 'http://www.eucharistiefeier.de/lk/api.php?format=json&' \
              f'info=wdtrgflu&dup=e&bahn=j&kal={self.kalender}&jahr={year}&'
        if month: url += f'monat={month}&'
        if month and day: url += f'tag={day}&'
        return requests.get(url)

    def request_cache(self, d: date) -> dict:
        """
        Erstellt das API-Format aus dem Cache. Falls benötigt wird dazu der
        Cache angelegt. Sollte kein Cache vorgesehen sein, wird direkt die
        Online-API abgefragt.
        """
        if self.cache_dir is None:
            return self.request_api(d.year, d.month, d.day)

        # Daten einlesen (ggf. herunterladen)
        dir = os.path.join(self.cache_dir, self.kalender)
        file = os.path.join(dir, f'{d.year}.json')
        if not os.path.exists(file):
            if not os.path.exists(dir): os.makedirs(dir)
            r = self.request_api(d.year)
            with open(file, 'wb') as f: f.write(r.content)
            data = r.json()
        else:
            with open(file) as f: data = json.load(f)

        # Dictionary für aktuellen Tag konstruieren
        datestr = d.isoformat()
        data['Zelebrationen'] = {k: v for k, v in data['Zelebrationen'].items()
                                 if datestr == v['Datum']}
        return data
