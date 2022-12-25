#!/usr/bin/env python
import time

from lib.carillon import Carillon
from lib.direktorium import TodayDirektorium

from customstriker import CustomStriker

if __name__ == '__main__':
    carillon = Carillon()
    direktorium = TodayDirektorium()

    striker = CustomStriker(carillon, direktorium)

    while True:
        time.sleep(1)
