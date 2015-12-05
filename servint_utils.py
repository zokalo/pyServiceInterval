#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application implementation classes.
"""
from copy import copy
from datetime import date, timedelta
import re

__author__ = 'Don D.S.'


class Operation(object):
    """ Represents service operation.

    Examples of using:
    # Create an operation type.
    >>> oil_change = Operation("Changing the oil: engine",
    ...                        period_km=10000,
    ...                        period_year=1)

    # Create done-operation copy from current operation type.
    >>> oil_changed = oil_change.done(
    ...     km=9842,
    ...     date=date.today(),
    ...     comment="Price: 4000 RUR")

    # Create readable form.
    >>> print(oil_changed)
    2015-12-05 / 9842.0 km
    Changing the oil: engine
    Every 1.0 year(s) or 10000.0 km
    Price: 4000 RUR
    >>> print(oil_change)
    Changing the oil: engine.
    Every 1.0 year(s) or 10000.0 km

    # Create representative form.
    >>> repr(oil_change)
    'Operation(Changing the oil: engine, period_km=10000.0, period_year=1.0)'

    """

    def __init__(self, label, period_km=0, period_year=0, period_month=0):
        """ Create service operation type.

        Default periods value is 0. It means that operation is non-periodic.

        :param label:        operation label or description
        :param period_km:    operation period by vehicle haul, km
        :param period_year:  operation period time, years
        :param period_month:  operation period time, months
        """
        super().__init__()
        # Initialize default values.
        self._label = ""
        self._period_time = timedelta()
        self._period_km = 0
        # For done copy of this operation type.
        self._done_at_km = 0
        self._done_at_date = None
        # Additional information (price, parts item numbers).
        self.comment = ""
        # Initialize private flag.
        self._is_done = False   # default operation state: not done.
        # Set up values for current operation instance.
        self.label = label
        self.period_time = timedelta(
            days=365 * period_year + 30.4 * period_month)
        self.period_km = period_km

    def done(self, km=0, date=None, comment=""):
        # Create a copy of this operation, that has been done and return it.
        done = copy(self)
        done.done_at_km = km
        done.done_at_date = date
        done.comment = comment
        done._is_done = True
        return done

    def undo(self):
        # Clear information about operation completion
        self.done_at_km = 0
        self.done_at_date = None
        self.comment = ""
        self._is_done = False

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
    def period_time(self):
        return self._period_time

    @period_time.setter
    def period_time(self, period):
        if not isinstance(period, timedelta):
            raise TypeError("Time must be represented as <datetime.timedelta>"
                            " class instance.")
        self._period_time = period

    @property
    def period_km(self):
        return self._period_km

    @period_km.setter
    def period_km(self, new_period):
        try:
            new_period = float(new_period)
        except ValueError:
            raise TypeError("Period must be a numeric type or string number.")
        if new_period < 0:
            raise ValueError("Operation period must be positive. "
                             "Received value " + str(new_period))
        self._period_km = new_period

    @property
    def done_at_km(self):

        return self._done_at_km

    @done_at_km.setter
    def done_at_km(self, new_km):
        try:
            new_km = float(new_km)
        except ValueError:
            raise TypeError(
                "Haul value must be a numeric type or string number.")
        # Haul can be negative if this field used to show relative distance
        # from planned maintenance.
        # if new_km < 0 and not relative:
        #     raise ValueError("Haul value must be positive. "
        #                      "Received value " + str(new_km))
        self._done_at_km = new_km

    @property
    def done_at_date(self):
        return self._done_at_date

    @done_at_date.setter
    def done_at_date(self, new_date):
        if isinstance(new_date, date):
            self._done_at_date = new_date
        else:
            raise TypeError("Date must be a <datetime.date> class instance.")

    def __eq__(self, other):
        return self.done_at_km == other.done_at_km

    def __ne__(self, other):
        return self.done_at_km != other.done_at_km

    def __lt__(self, other):
        return self.done_at_km < other.done_at_km

    def __le__(self, other):
        return self.done_at_km <= other.done_at_km

    def __gt__(self, other):
        return self.done_at_km >= other.done_at_km

    def __ge__(self, other):
        return self.done_at_km > other.done_at_km

    def __repr__(self):
        if self.is_done:
            return "Operation({0}, period_km={1}, period_year={2}).done("\
                   "km={3}, date={4}, comment={5})".format(
                       self.label, self.period_km, self.period_time.days/365,
                       self.done_at_km, self.done_at_date, self.comment)
        else:
            return "Operation({0}, period_km={1}, period_year={2})".format(
                self.label, self.period_km, self.period_time.days/365)


    def __str__(self):
        """ !!! ATTENTION !!!
        If you change this method, you also need to change OperationList.load()
        parsing method. This is bad idea.
        """
        period_months = round(self.period_time.days/(365/12))

        if self.is_done:
            return "{date} / {km} km\n" \
                   "{label}\n" \
                   "Every {prd_time} or {prd_km} km\n"\
                   "{comment}".format(
                       label=self.label,
                       date=self.done_at_date.isoformat(),
                       km=self.done_at_km,
                       comment=self.comment,
                       prd_time=
                       str(period_months) + " month(s)" if period_months < 12
                       else str(round(period_months/12, 1)) + " year(s)",
                       prd_km=self.period_km)
        else:

            return "{label}.\nEvery {prd_time} or {prd_km} km".format(
                label=self.label,
                prd_time=str(period_months) + " month(s)" if period_months < 12
                else
                str(round(period_months/12, 1)) + " year(s)",
                prd_km=self.period_km)


class OperationsList(list):
    """ List inheritance with additional methods.
    Added save(), load() methods.

    Example of using:
    >>> operations = OperationsList([
    ...     Operation("Changing the oil: engine", 1, 10000),
    ...     Operation("Changing the oil: gearbox", 3, 45000)])

    >>> operations.save("doctest.txt")
    """
    def __init__(self, seq=()):
        super().__init__(seq)

    def save(self, file):
        """ Create human-readable text file from list
        """
        with open(file, 'w') as fh:
            for operation in self:
                print(operation, end="\n\n", file=fh)

    @staticmethod
    def load(file):
        """ Create <OperationList> class instance from file previously created
        by self.save() or created manually with the same formatting.

        # Create test operation type.
        >>> oil_change = Operation("Changing the oil: engine",
        ...                        period_km=10000,
        ...                        period_year=1)

        # Create done-operation copy from current test operation type.
        >>> oil_changed = oil_change.done(
        ...     km=9842,
        ...     date=date.today(),
        ...     comment="Price: 4000 RUR")

        # Format for operation that has been done:
        >>> print(oil_changed)
        2015-12-05 / 9842.0 km
        Changing the oil: engine
        Every 1.0 year(s) or 10000.0 km
        Price: 4000 RUR
        >>> OperationsList([oil_changed]).save('doctest.txt')

        # Doctest for reading and parsing operation that has been done:
        >>> print(OperationsList.load('doctest.txt'))
        [Operation(Changing the oil: engine, period_km=10000.0, period_year=1.0).done(km=9842.0, date=2015-12-05, comment=None)]

        # Format for operation that hasn't been done:
        >>> print(oil_change)
        Changing the oil: engine.
        Every 1.0 year(s) or 10000.0 km
        >>> OperationsList([oil_change]).save('doctest.txt')

        # Doctest for reading and parsing operation that hasn't been done:
        >>> print(OperationsList.load('doctest.txt'))
        [Operation(Changing the oil: engine., period_km=10000.0, period_year=1.0)]
        """
        # Regular expression that can detect, that operation has been done
        re_done = re.compile(
            r"(?P<yyyy>[0-9]{4})-(?P<mm>[0-9]{2})-(?P<dd>[0-9]{2})\s/\s(?P<km>[0-9.]+)\skm")
        # Regular expression that can detect operation periods line
        re_period = re.compile(
            r"Every\s(?P<time>[0-9.]+)\s(?P<year_or_mon>[a-z()]+)\sor\s(?P<km>[0-9.]+)\skm")
        # Output variable
        ops = OperationsList()
        # Operation arguments
        label = None
        period_km = None
        period_year = None
        period_month = None
        done_at_km = None
        done_at_date = None
        comment = None
        # Operation done flag
        is_done = False
        # Control line numbers
        nline_done_first = None
        with open(file, 'r') as fh:
            for num, line in enumerate(fh):
                line = line.strip('\n')
                # At first line and after every empty line...
                if line == "":
                    # ...append previous operation to list (if exist)
                    if label:  # (check by label - it is necessary argument)
                        op = Operation(label,
                                       period_km,
                                       period_year,
                                       period_month)
                        if is_done:
                            op = op.done(done_at_km,
                                         done_at_date,
                                         comment)
                        ops.append(op)
                    # ... and reset operation args, flag, nlines - anyway
                    # Operation arguments
                    label = None
                    period_km = None
                    period_year = None
                    period_month = None
                    done_at_km = None
                    done_at_date = None
                    comment = None
                    # Operation done flag
                    is_done = False
                    # Control line numbers
                    nline_done_first = None
                # Match with done-type operation
                match_done = re_done.search(line)
                if match_done:
                    is_done = True
                    done_at_km = float(match_done.group('km'))
                    done_at_date = date(int(match_done.group('yyyy')),
                                        int(match_done.group('mm')),
                                        int(match_done.group('dd')))
                    nline_done_first = num
                # Next line after match_done line - is label
                if match_done and num - 1 == nline_done_first:
                    label = line
                # Check for periods line
                match_period = re_period.search(line)
                if match_period:
                    year_or_mon = match_period.group('year_or_mon')
                    if year_or_mon == "year(s)":
                        period_year = float(match_period.group('time'))
                        period_month = 0
                    elif year_or_mon == "month(s)":
                        period_year = 0
                        period_month = float(match_period.group('time'))
                    else:
                        raise ValueError("Unable to parse line: \n" + line)
                    period_km = float(match_period.group('km'))

                    if not match_done:
                        label = line_previous
                # Next line after label - is periods. Already parsed.
                # Next line after periods - is comment
                if match_done and num - 3 == nline_done_first:
                    comment = line
                # Keep previous line. We can detect operation that hasn't been
                # done only from second string. In this case previous line will
                # be used as label.
                line_previous = line
        return ops


# List of all available operations
PERIODICAL_OPERATIONS_CAT = [
    Operation("Changing the oil: engine", 1, 10000),
]
# ToDo: import/export catalogue to human-readable txt-file.


class VehicleLogBook(object):
    """ Represents storage of service operations for vehicle

    Vehicle identified by text label and production date

    Examples of using:
    # Without periodical operations catalogue.
    >>> car = VehicleLogBook(
    ...     "Hyundai Getz",
    ...     date(year=2006, month=11, day=30))

    # Or with catalogue.
    >>> car = VehicleLogBook(
    ...     "Hyundai Getz",
    ...     date(year=2006, month=11, day=30),
    ...     PERIODICAL_OPERATIONS_CAT)

    # Add complete operation.
    # ...Prepare operation type.
    >>> oil_change = Operation("Changing the oil: engine",
    ...                        period_km=10000,
    ...                        period_year=1)

    # ...Prepare operation instance.
    >>> oil_changed = oil_change.done(
    ...     km=98042,
    ...     date=date.today(),
    ...     comment="Price: 4000 RUR")

    # ...Add operation to log.
    >>> car.add_operation_to_log(oil_changed)

    # Make maintenance plan.
    >>> car.make_maintenance_plan()
    [Operation(Changing the oil: engine, period_km=10000.0, period_year=1.0).done(km=108042.0, date=2016-12-04, comment=)]

    # Add new periodic operation to catalogue.
    # ...already exist in catalogue
    >>> car.add_operation_to_cat(oil_change)

    # ...new operation
    >>> oil_change_gb = Operation("Changing the oil: gearbox",
    ...                        period_km=45000,
    ...                        period_year=3)

    >>> car.add_operation_to_cat(oil_change_gb)

    """
    def __init__(self, label, production_date, operations_cat=tuple()):
        """
        :param label:            vehicle text identifier
        :param production_date:  vehicle production date as <datetime.date>
                                 class instance
        :param operations_cat:   catalogue of all periodical operations types
                                 (iterable with items - instances of <Operation>
                                 class)
        """
        super().__init__()
        # Car label
        self.label = label
        # Car production date.
        if isinstance(production_date, date):
            self._production_date = production_date
        else:
            raise TypeError("Argument <production_date> must be an instance "
                            "of <datetime.date> type.")
        # List of all done operations for keeping history.
        self._operations_log = OperationsList()
        # Catalogue of all periodical operations types.
        # keys - operation labels; values - <Operation> class instances.
        self._operations_cat = dict()
        for op in operations_cat:
            if op.period_time == 0 and op.period_km == 0:
                raise TypeError(
                    "Operation <{}> is not periodic.".format(op.label) +
                    "\nUnable to add non-periodic operation to the catalogue "
                    "of periodic operations.")
            self._operations_cat[op.label] = op

    def add_operation_to_log(self, operation):
        if not isinstance(operation, Operation):
            raise TypeError("Argument <operation> must be an instance "
                            "of <Operation> type.")
        if not operation.is_done:
            # It matter that operation has never been done.
            raise ValueError("Operation date and haul not specified. "
                             "Unable to add operation that has never been "
                             "done.")
        # Put operation to the log-list.
        self._operations_log.append(operation)
        # If it is periodical operation
        if operation.label in self._operations_cat:
            # Update last completion time for this operation
            # if that is newer than last.
            operation_last = self._operations_cat[operation.label]
            if operation > operation_last:
                self._operations_cat[operation.label] = operation

    def add_operation_to_cat(self, operation):
        if operation not in self._operations_cat.values():
            # Default operation last completion date/haul
            last_date = self._production_date
            last_km = 0
            # Lookup operations log for a last operation with the same label
            same_operations = list(filter(lambda x: x.label == operation.label,
                                          self._operations_log))
            if len(same_operations) > 0:
                last_operation = max(same_operations)
                last_date = last_operation.done_at_date
                last_km = last_operation.done_at_km
            # Set operation last completion
            operation = operation.done(last_km, last_date)
            # Add operation to periodic operations catalogue
            self._operations_cat[operation.label] = operation

    def clear_log(self):
        # Clear log of produced operations.
        self._operations_log.clear()
        # Clear information about last operation completion
        for operation in self._operations_cat.values():
            operation.undo()

    def clear_all(self):
        # Clear operations log and peridic operations catalogue.
        self._operations_log.clear()
        self._operations_cat.clear()

    def make_maintenance_plan(self, haul=None):
        """ Make plan of periodic operations that must be performed.

        If current haul is specified, function returns the plan with operations
        planned with haul relative to current.
        Otherwise - with absolute haul values.

        :param haul:  (unnecessary) current vehicle haul, km.
        :return:  list of operations, that represents plan of periodic
                  operations that must be performed.
        """
        plan = list()
        for operation in self._operations_cat.values():
            # Planned operation date.
            last_date = operation.done_at_date
            period_date = operation.period_time
            plan_date = last_date + period_date

            # Planned operation haul.
            last_km = operation.done_at_km
            period_km = operation.period_km
            plan_km = last_km + period_km

            # Make planned operation haul relative to current.
            if haul:
                plan_km -= haul
            plan.append(operation.done(plan_km, plan_date))
        return plan

    def export_log(self, file):
        # Export operations history to txt file.
        self._operations_log.save(file)

    def export_cat(self, file):
        # Export periodic operations catalogue to txt file.
        cat = self._operations_cat.values()
        # Clear last operation info and convert it to <OperationsList> type.
        cat = OperationsList([x.undo() for x in cat])
        cat.save(file)

    def import_log(self, file):
        self._operations_log.load(file)

    def import_cat(self, file):
        cat = OperationsList(self._operations_cat.values())
        cat.load(file)

    # ToDo: serialize VehicleLogBook to file with the same name as label


if __name__ == "__main__":
    # If running that module as the main program - do doctests.
    import doctest
    doctest.testmod()
