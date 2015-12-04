#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application implementation classes.
"""
from collections import defaultdict, namedtuple
from copy import copy
import time

__author__ = 'Don D.S.'


class Operation(object):
    """ Represents service operation.

    Example of using:
    # 1. Create an operation type
    >>> oil_change = Operation("Changing the oil: engine", 1, 10000)

    # 2. Create done-operation from current operation type
    >>> operation = oil_change.done(km=9842, date=time.localtime())

    """

    def __init__(self, label, period_km, period_year):
        # Initialize default values.
        self._label = ""
        self._period_year = 0
        self._period_km = 0
        self._done_km = 0       # For done copy
        self._done_date = None  # of this operation type.
        # Initialize private flag.
        self._is_done = False   # default operation state: not done
        # Set up real values.
        self.label = label
        self.period_year = period_year
        self.period_km = period_km

    def done(self, km=0, date=None):
        # Create a copy of this operation, that has been done and return it.
        done = copy(self)
        done.done_km = km
        done.done_date = date
        done._is_done = True
        return done

    @property
    def is_done(self):
        # Flag: is operation has been done?
        return self._is_done

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_title):
        if isinstance(new_title, str):
            self._label = new_title
        else:
            raise TypeError("OperationType title must be a text string.")

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
        return self._period_km

    @period_km.setter
    def period_km(self, new_period):
        try:
            self._period_km = float(new_period)
        except ValueError:
            raise TypeError("Period must be a numeric type or string number.")

    @property
    def done_km(self):
        return self._done_km

    @done_km.setter
    def done_km(self, new_km):
        self._done_km = new_km

    @property
    def done_date(self):
        return self._done_date

    @done_date.setter
    def done_date(self, new_date):
        if isinstance(new_date, time.struct_time):
            self._done_date = new_date
        else:
            raise TypeError("Date must be a <time.struct_time> type instance.")

    def __eq__(self, other):
        return self.done_km == other.done_km

    def __ne__(self, other):
        return self.done_km != other.done_km

    def __lt__(self, other):
        return self.done_km < other.done_km

    def __le__(self, other):
        return self.done_km <= other.done_km

    def __gt__(self, other):
        return self.done_km >= other.done_km

    def __ge__(self, other):
        return self.done_km > other.done_km


# List of all available operations
PERIODICAL_OPERATIONS_CAT = [
    Operation("Changing the oil: engine", 1, 10000),
]
# ToDo: import/export catalogue to human-readable txt-file.


class VehicleLogBook(object):
    """ Represents storage of service operations for vehicle

    Vehicle identified by text label and production date

    Example of using:
    # Without periodical operations catalogue.
    >>> car = VehicleLogBook("Hyundai Getz", time.strptime("30-11-2006", "%d-%m-%Y"))

    # Or with catalogue.
    >>> car = VehicleLogBook(
    ...     "Hyundai Getz",
    ...     time.strptime("30-11-2006", "%d-%m-%Y"),
    ...     PERIODICAL_OPERATIONS_CAT)
    """
    def __init__(self, label, production_date, operations_cat=tuple()):
        """
        :param label:            vehicle text identifier
        :param production_date:  vehicle production date
        :param operations_cat:   catalogue of all periodical operations types
        """
        # Car label
        self.label = label
        # Car production date.
        if isinstance(production_date, time.struct_time):
            self._production_date = production_date
        else:
            raise TypeError("Argument <production_date> must be an instance of <time.struct_time> type.")
        # List of all done operations for keeping history.
        self._operations_log = list()
        # Catalogue of all periodical operations types
        self._operations_cat = dict()
        for op in operations_cat:
            if op.period_year == 0 and op.period_km == 0:
                raise TypeError("Operation <{}> is not periodic.".format(op.label))
            self._operations_cat[op.label] = op

    def add_operation_to_log(self, operation):
        if not isinstance(operation, Operation):
            raise TypeError("Argument <operation> must be an instance of <Operation> type.")
        if not operation.is_done:
            # It matter that operation has never been done.
            raise ValueError("Operation date and haul (km) not specified.")
        # Put operation to the log-list.
        self._operations_log.append(operation)
        # If it is periodical operation
        if operation.label in self._operations_cat:
            # Update last completion time for this operation if that is newer than last.
            operation_last = self._operations_cat[operation.label]
            if operation > operation_last:
                self._operations_cat[operation.label] = operation

    # ToDo: method for edit log and cat. If added to cat, need to find this operation label in log and find the latest.

    def clear(self):
        self._operations_log.clear()
        # ToDo: also reset to zero self._operations_cat dates (=None) and hauls (=0) of last done

    def next_maintenance(self, current_haul_km):
        # Return forecast about the next preventive maintenance.
        pass


if __name__ == "__main__":
    # If running that module as the main program - do doctests.
    import doctest
    doctest.testmod()