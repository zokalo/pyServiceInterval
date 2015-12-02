#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application implementation classes.
"""
from collections import defaultdict, namedtuple

__author__ = 'Don D.S.'


class Operation(object):
    # Represents service operation

    def __init__(self, title, period_year, period_km):
        # Initialize default values
        self._title = ""
        self._period_year = 0
        self._period_km = 0
        # Set up real values
        self.title = title
        self.period_year = period_year
        self.period_km = period_km

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, new_title):
        if isinstance(new_title, str):
            self._title = new_title
        else:
            raise TypeError("Operation title must be a text string.")

    @property
    def period_year(self):
        return self._period_year

    @period_year.setter
    def period_year(self, new_period):
        try:
            self._period_year = float(new_period)
        except ValueError:
            raise TypeError("Period must be a numeric type or string number.")

    @property
    def period_km(self):
        return self.period_km

    @period_year.setter
    def period_km(self, new_period):
        try:
            self.period_km = float(new_period)
        except ValueError:
            raise TypeError("Period must be a numeric type or string number.")


# List of all available operations
OPERATIONS_CATALOGUE = [
    Operation("Changing the oil: engine", 1, 10000),
]
# ToDo: import/export catalogue to human-readable txt-file.


class VehicleLogBook(object):
    # Represents storage of service operations
    def __init__(self, production_date):
        # ToDo: process different timeformats
        # Car production date.
        self.prod_date = production_date
        # Information about operation.
        Info = namedtuple('Info', ['date', 'haul'])
        # Dictionary of operations.
        self.operations = defaultdict(lambda: Info(date=self.prod_date, haul=0))

    def next_maintenance(self, current_haul_km):
        # Return forecast about the next preventive maintenance.
        pass