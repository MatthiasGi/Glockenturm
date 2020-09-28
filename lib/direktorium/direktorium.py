from datetime import date
import requests
from typing import List

from .event import Event


class Direktorium:

    def __init__(self, kalender='deutschland'):
        self.kalender = kalender

    def get(self, d: date) -> List[Event]:
        r = requests.get('http://www.eucharistiefeier.de/lk/api.php?'
                         'format=json&info=wdtrgflu&dup=e&bahn=j&'
                         f'kal={self.kalender}&'
                         f'jahr={d.year}&monat={d.month}&tag={d.day}')
        entries = [Event.parse(e) for e in r.json()['Zelebrationen'].values()]
        entries.sort(key=lambda e: e.importance)
        return entries
