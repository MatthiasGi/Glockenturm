from datetime import datetime, timedelta
import schedule
from threading import Thread
import time


class QuarterClock:
    """
    Einfacher „Mechanismus“, der jede Viertelstunde auslöst. Dabei werden dann
    die Observer getriggert, die zuvor hinzugefügt wurden.

    Attributes
    ----------
    _observers : List[QuarterClockObserver]
        Liste der auszulösenden Observer.

    Methods
    -------
    attach_observer(observer, priority)
        Reiht einen Observer ein, der später mit steigender Priorität
        aufgerufen wird.
    remove_observer(observer)
        Entfernt einen Observer wieder aus der Liste.
    _trigger()
        Interne Methode, die jede Viertelstunde ausgelöst wird.
    """

    def __init__(self):
        """
        Bereitet das Objekt vor, indem die Observerliste, der Scheduler für die
        viertelstündigen Aktionen und ein den Scheduler immer wieder
        aufrufender Thread eingerichtet werden.
        """
        self._observers = []

        for t in range(0, 60, 15):
            schedule.every().hour.at(':%02d' % t).do(self._trigger)

        def thread():
            while True:
                schedule.run_pending()
                time.sleep(0.1)

        Thread(target=thread, daemon=True).start()

    def attach_observer(
        self, observer: 'QuarterClockObserver', priority: int = None
    ) -> None:
        """
        Fügt einen Observer der Liste der zu unterichtenden Observer hinzu.

        Parameters
        ----------
        observer : QuarterClockObserver
            Observer, der hinzugefügt werden soll.
        priority : int (optional)
            Priorität, mit der der Observer aufgerufen werden soll. Höhere
            Priorität bedeutet dabei frühere Bearbeitung. Wird diese nicht
            übergeben, wird der Observer an das Ende der Liste gestellt. Zur
            Änderung einer zuvor festgelegten Priorität muss der Observer
            entfernt und neu hinzugefügt werden.

        Raises
        ------
        ValueError
            Falls der Observer bereits hinzugefügt war.
        """
        if next((o for o in self._observers if o[1] == observer), None):
            raise ValueError('Observer ist bereits in der Liste!')
        if priority is None:
            priority = -self._observers[-1][0] - 1 if self._observers else 0
        self._observers.append((-priority, observer))
        self._ovservers.sort()

    def remove_observer(self, observer: 'QuarterClockObserver') -> None:
        """
        Entfernt den übergebenen Observer wieder aus der Liste.

        Parameters
        ----------
        observer : QuarterClockObserver
            Der zu entfernende Observer. Wurde dieser nicht gefunden, passiert
            nichts.
        """
        o = next((o for o in self._observers if o[1] == observer), None)
        if o: self._observers.remove(o)

    def _trigger(self) -> None:
        """
        Interne Methode, die viertelstündig ausgelöst wird. Sie informiert die
        Observer über die Stundenzahl (24-Stundenformat) und über die Anzahl an
        vergangenen Viertelstunden.
        """
        time = datetime.now() + timedelta(minutes=7, seconds=30)
        hours, quarters = time.hour, time.minute // 15
        for o in self._observers:
            if not o.trigger(hours, quarters): return


class QuarterClockObserver:
    """
    Einfaches Objekt, das über Viertelstundenauslösung der `QuarterClock`
    informiert wird.

    Methods
    -------
    trigger(hours, quarters) : bool
        Wird über Viertelstundenauslösungen informiet.
    """

    def trigger(self, hours: int, quarters: int) -> bool:
        """
        Wird jede Viertelstunde ausgelöst. Soll zurückgeben, ob die weitere
        Abarbeitung erfolgen soll.

        Parameters
        ----------
        hours : int
            Stundenzahl im 24-Stundenformat.
        quarters : int
            Anzahl der Viertelstunden (also HH:00, HH:15, HH:30, HH:45).

        Returns
        -------
        Ob die weitere Abarbeitung der Observerliste erfolgen soll. So lässt
        sich die Abarbeitung beispielsweise abbrechen, wenn ein später
        erfolgtes Geläut eigentlich schweigen soll.
        """
        return True
