from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import schedule
from threading import Thread
import time


class Striker(ABC):
    """
    Einfache Klasse, die jede Viertelstunde ausgelöst wird. Durch
    Implementierung dieser abstrakten Klasse realisiert der Nutzer dann das
    eigentliche Geläut.

    Methods
    -------
    strike(hours, quarters)
        Wird bei Viertelstundenauslösung ausgeführt.
    _strike()
        Interne Metode zur Auslösung der abstrakten Methode
        `strike(hours, quarters)`.
    """

    def __init__(self):
        """
        Initialisiert das Objekt und bereitet Scheduler und Thread zu dessen
        Prüfung vor.
        """
        for t in range(0, 60, 15):
            schedule.every().hour.at(f':{t:02d}').do(self._strike)

        def thread():
            while True:
                schedule.run_pending()
                time.sleep(0.1)

        Thread(target=thread, daemon=True).start()

    @abstractmethod
    def strike(self, hours: int, quarters: int) -> None:
        """
        Durch die implementierende Klasse umzusetzende Methode, die Anzahl an
        Stunden (im 24-Stunden-Format) und voller Viertelstunden erhält.

        Parameters
        ----------
        hours : int
            Anzahl an Stunden im 24-Stunden-Format.
        quarters : int
            Anzahl der vollen Viertelstunden.
        """
        pass

    def _strike(self) -> None:
        """
        Interne Methode, die jede Viertelstunde aufgerufen wird und die zu
        implementierende Methode `strike` mit den nötigen Parametern aufruft.
        """
        time = datetime.now() + timedelta(minutes=7, seconds=30)
        self.strike(time.hour, time.minute // 15)
