#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ServiceInterval
Application implementation classes.
"""
from copy import copy
from datetime import date, timedelta
import gzip
from numbers import Number
import os
import pickle
import re
import warnings

__author__ = 'Don D.S.'

# Version of ServiceInterval.
_VERSION = (1, 0)


class Operation(object):
    """ Represents service operation.

    Examples of using:
    # Create an operation type.
    >>> oil_change = Operation("Changing the oil: engine",
    ...                        interval_km=10000,
    ...                        interval_year=1)

    # Create done-operation copy from current operation type.
    >>> oil_changed = oil_change.done(
    ...     km=9842,
    ...     date=date(2015, 12, 5),
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
    'Operation(Changing the oil: engine, interval_km=10000.0, interval_year=1.0)'

    """

    def __init__(self, label, interval_km=0, interval_year=0, interval_month=0):
        """ Create service operation type.

        Default intervals value is 0. It means that operation is non-periodic.

        :param label:          operation label or description
        :param interval_km:    operation interval by vehicle haul, km
        :param interval_year:  operation interval time, years
        :param interval_month: operation interval time, months
        """
        super().__init__()
        # Initialize default values.
        self._label = ""
        self._interval_time = timedelta()
        self._interval_km = 0
        # For done copy of this operation type.
        self._done_at_km = 0
        self._done_at_date = None
        # Additional information (price, parts item numbers).
        self.comment = ""
        # Initialize private flag.
        self._is_done = False   # default operation state: not done.
        # Set up values for current operation instance.
        self.label = label
        self.interval_time = timedelta(
            days=365 * interval_year + 30.4 * interval_month)
        self.interval_km = interval_km

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
    def is_periodic(self):
        return self.interval_km != 0

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
    def interval_time(self):
        return self._interval_time

    @interval_time.setter
    def interval_time(self, interval):
        if not isinstance(interval, timedelta):
            raise TypeError("Time must be represented as <datetime.timedelta>"
                            " class instance.")
        self._interval_time = interval

    @property
    def interval_km(self):
        return self._interval_km

    @interval_km.setter
    def interval_km(self, new_interval):
        try:
            new_interval = float(new_interval)
        except ValueError:
            raise TypeError("Interval must be a numeric type or string number.")
        if new_interval < 0:
            raise ValueError("Operation interval must be positive. "
                             "Received value " + str(new_interval))
        self._interval_km = new_interval

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
            return "Operation({0}, interval_km={1}, interval_year={2}).done("\
                   "km={3}, date={4}, comment={5})".format(
                       self.label, self.interval_km, self.interval_time.days/365,
                       self.done_at_km, self.done_at_date, self.comment)
        else:
            return "Operation({0}, interval_km={1}, interval_year={2})".format(
                self.label, self.interval_km, self.interval_time.days/365)

    def __str__(self):
        """ !!! ATTENTION !!!
        If you change this method, you also need to change OperationList.load()
        parsing method. This is bad idea.
        """
        interval_months = round(self.interval_time.days/(365/12))

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
                       str(interval_months) + " month(s)" if interval_months < 12
                       else str(round(interval_months/12, 1)) + " year(s)",
                       prd_km=self.interval_km)
        else:

            return "{label}.\nEvery {prd_time} or {prd_km} km".format(
                label=self.label,
                prd_time=str(interval_months) + " month(s)" if interval_months < 12
                else
                str(round(interval_months/12, 1)) + " year(s)",
                prd_km=self.interval_km)


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
        ...                        interval_km=10000,
        ...                        interval_year=1)

        # Create done-operation copy from current test operation type.
        >>> oil_changed = oil_change.done(
        ...     km=9842,
        ...     date=date(2015, 12, 5),
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
        [Operation(Changing the oil: engine, interval_km=10000.0, interval_year=1.0).done(km=9842.0, date=2015-12-05, comment=None)]

        # Format for operation that hasn't been done:
        >>> print(oil_change)
        Changing the oil: engine.
        Every 1.0 year(s) or 10000.0 km
        >>> OperationsList([oil_change]).save('doctest.txt')

        # Doctest for reading and parsing operation that hasn't been done:
        >>> print(OperationsList.load('doctest.txt'))
        [Operation(Changing the oil: engine., interval_km=10000.0, interval_year=1.0)]
        """
        # Regular expression that can detect, that operation has been done
        re_done = re.compile(
            r"(?P<yyyy>[0-9]{4})-(?P<mm>[0-9]{2})-(?P<dd>[0-9]{2})\s/\s(?P<km>[0-9.]+)\skm")
        # Regular expression that can detect operation intervals line
        re_interval = re.compile(
            r"Every\s(?P<time>[0-9.]+)\s(?P<year_or_mon>[a-z()]+)\sor\s(?P<km>[0-9.]+)\skm")
        # Output variable
        ops = OperationsList()
        # Operation arguments
        label = None
        interval_km = None
        interval_year = None
        interval_month = None
        done_at_km = None
        done_at_date = None
        comment = None
        # Operation done flag
        is_done = False
        # Control line numbers
        nline_done_first = None
        # Initialize storage
        line_previous = ""
        with open(file, 'r') as fh:
            for num, line in enumerate(fh):
                line = line.strip('\n')
                # At first line and after every empty line...
                if line == "":
                    # ...append previous operation to list (if exist)
                    if label:  # (check by label - it is necessary argument)
                        op = Operation(label,
                                       interval_km,
                                       interval_year,
                                       interval_month)
                        if is_done:
                            op = op.done(done_at_km,
                                         done_at_date,
                                         comment)
                        ops.append(op)
                    # ... and reset operation args, flag, nlines - anyway
                    # Operation arguments
                    label = None
                    interval_km = None
                    interval_year = None
                    interval_month = None
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
                    done_at_km = int(float(match_done.group('km')))
                    done_at_date = date(int(match_done.group('yyyy')),
                                        int(match_done.group('mm')),
                                        int(match_done.group('dd')))
                    nline_done_first = num
                # Next line after match_done line - is label
                if match_done and num - 1 == nline_done_first:
                    label = line
                # Check for intervals line
                match_interval = re_interval.search(line)
                if match_interval:
                    year_or_mon = match_interval.group('year_or_mon')
                    if year_or_mon == "year(s)":
                        interval_year = float(match_interval.group('time'))
                        interval_month = 0
                    elif year_or_mon == "month(s)":
                        interval_year = 0
                        interval_month = float(match_interval.group('time'))
                    else:
                        raise ValueError("Unable to parse line: \n" + line)
                    interval_km = int(float(match_interval.group('km')))

                    if not match_done:
                        label = line_previous
                # Next line after label - is intervals. Already parsed.
                # Next line after intervals - is comment
                if match_done and num - 3 == nline_done_first:
                    comment = line
                # Keep previous line. We can detect operation that hasn't been
                # done only from second string. In this case previous line will
                # be used as label.
                line_previous = line
        return ops


class VehicleLogBook(object):
    """ Represents storage of service operations for vehicle

    Vehicle identified by text label and production date

    WARNING!!! If you add some methods, do not forget to update
    self._changed field, that shows that object contains unsaved changes!

    Examples of using:
    # Without periodical operations catalogue.
    >>> car = VehicleLogBook(
    ...     "Hyundai Getz",
    ...     date(year=2006, month=11, day=30))

    # Or with catalogue.
    >>> catalogue = OperationsList([
    ...     Operation("Changing the oil: engine", 1, 10000),])
    >>> car = VehicleLogBook(
    ...     "Hyundai Getz",
    ...     date(year=2006, month=11, day=30),
    ...     catalogue)

    # Add complete operation.
    # ...Prepare operation type.
    >>> oil_change = Operation("Changing the oil: engine",
    ...                        interval_km=10000,
    ...                        interval_year=1)

    # ...Prepare operation instance.
    >>> oil_changed = oil_change.done(
    ...     km=98042,
    ...     date=date(2015, 12, 5),
    ...     comment="Price: 4000 RUR")

    # ...Add operation to log.
    >>> car.add_operation_to_log(oil_changed)

    # Make maintenance plan.
    >>> car.make_maintenance_plan()
    [Operation(Changing the oil: engine, interval_km=10000.0, interval_year=1.0).done(km=108042.0, date=2016-12-04, comment=)]

    # Add new periodic operation to catalogue.
    # ...already exist in catalogue
    >>> car.add_operation_to_cat(oil_change)

    # ...new operation
    >>> oil_change_gb = Operation("Changing the oil: gearbox",
    ...                        interval_km=45000,
    ...                        interval_year=3)

    >>> car.add_operation_to_cat(oil_change_gb)

    # Serialize (save) class instance to file.
    >>> car.save("doctest")

    # Deserialize (load) class instance from file
    >>> print(VehicleLogBook.load("doctest"))
    [Operation(Changing the oil: engine, interval_km=10000.0, interval_year=1.0).done(km=98042.0, date=2015-12-05, comment=Price: 4000 RUR)]

    """
    # Extension for files of class serialization
    _extension = ".sif"
    # Version identifier
    _version = _VERSION

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
        self._production_date = None
        self._filename = ""  # filename where object saved
        # Car label
        self._label = label
        self.production_date = production_date
        # Car haul today
        self._haul = 0
        # List of all done operations for keeping history.
        self._operations_log = OperationsList()
        # Catalogue of all periodical operations types.
        # keys - operation labels; values - <Operation> class instances.
        self._operations_cat = dict()
        for op in operations_cat:
            if op.interval_time == 0 and op.interval_km == 0:
                raise TypeError(
                    "Operation <{}> is not periodic.".format(op.label) +
                    "\nUnable to add non-periodic operation to the catalogue "
                    "of periodic operations.")
            self._operations_cat[op.label] = op
        self._modified = False  # WARNING!!! False in spite of assignation
        # label and production_date during call __init___(). Becomes True after
        # assignment this fields through properties.

    @property
    def haul(self):
        return self._haul

    @haul.setter
    def haul(self, new_haul):
        if isinstance(new_haul, str) and new_haul.isdigit():
            new_haul = float(new_haul)
        if isinstance(new_haul, Number):
            self._haul = new_haul
            self._modified = True
        else:
            raise TypeError(
                "Haul value must be a Number (int, float, ...) or digit-string")

    @property
    def extension(self):
        return self._extension

    @property
    def filename(self):
        return self._filename

    @property
    def is_modified(self):
        return self._modified

    @property
    def label(self):
        return self._label

    @label.setter
    def label(self, new_label):
        if self._label != new_label:
            self._modified = True
            self._label = new_label

    @property
    def production_date(self):
        return self._production_date

    @production_date.setter
    def production_date(self, new_prod_date):
        # Car production date.
        if isinstance(new_prod_date, date):
            if new_prod_date != self._production_date:
                self._modified = True
                self._production_date = new_prod_date
        else:
            raise TypeError("Argument <new_prod_date> must be an instance "
                            "of <datetime.date> type.")

    def get_all_oper_labels(self):
        """ Get set of all known operation labels
        :return: set of strings
        """
        labels = set()
        labels = labels.union([x.label for x in self._operations_log])
        labels = labels.union([x for x in self._operations_cat.keys()])
        return labels

    def get_periodic(self, label):
        """ Find periodic operation with the same label in periodic
        operations catalogue

        :param label:  String of operation label
        :return:       Operation instance or None (if no same label)
        """
        if label in self._operations_cat:
            return self._operations_cat[label]
        else:
            return None

    def add_operation_to_log(self, operation):
        if not isinstance(operation, Operation):
            raise TypeError("Argument <operation> must be an instance "
                            "of <Operation> type.")
        if not operation.is_done:
            # It matter that operation has never been done.
            raise ValueError("Operation date and haul not specified. "
                             "Unable to add operation that has never been "
                             "done.")
        self._modified = True
        # Put operation to the log-list.
        self._operations_log.append(operation)
        # If it is periodical operation
        if operation.is_periodic:
            if operation.label in self._operations_cat:
                # Update last completion time for this operation
                # if that is newer than last.
                operation_last = self._operations_cat[operation.label]
                if operation > operation_last:
                    self._operations_cat[operation.label] = operation
            else:
                # Add operation to periodic operations catalogue
                self.add_operation_to_cat(operation)

    def add_operation_to_cat(self, operation):
        if operation not in self._operations_cat.values():
            self._modified = True
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
        self._modified = True
        # Clear log of produced operations.
        self._operations_log.clear()
        # Clear information about last operation completion
        for operation in self._operations_cat.values():
            operation.undo()

    def clear_all(self):
        self._modified = True
        # Clear operations log and peridic operations catalogue.
        self._operations_log.clear()
        self._operations_cat.clear()

    def make_maintenance_plan(self, haul=None, relative=True):
        """ Make plan of periodic operations that must be performed.

        :param haul:  current vehicle haul, km. If you specify it here, than
                      this value will be saved in class property <haul>
        :param relative: If True, than the plan with operations planned with
                         haul relative to current.
                         Otherwise - with absolute haul values
        :return:  list of operations, that represents plan of periodic
                  operations that must be performed.
        """
        plan = list()
        if haul:
            self.haul = haul
        for operation in self._operations_cat.values():
            # Planned operation date.
            last_date = operation.done_at_date
            interval_date = operation.interval_time
            plan_date = last_date + interval_date

            # Planned operation haul.
            last_km = operation.done_at_km
            interval_km = operation.interval_km
            plan_km = last_km + interval_km

            # Make planned operation haul relative to current.
            if relative:
                plan_km -= self.haul
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
        self._modified = True
        # Import operations history from txt file.
        ops = OperationsList.load(file)
        for op in ops:
            self.add_operation_to_log(op)

    def import_cat(self, file):
        self._modified = True
        # Import periodic operations catalogue to txt file.
        ops = OperationsList.load(file)
        for op in ops:
            self.add_operation_to_cat(op)

    def save(self, file=None):
        """ Serialize current class instance.

        Saving using pickle as compressed file
        """
        # Make filename correct.
        if not file and not self._filename:
            raise ValueError("File name argument missed.")
        elif not file:
            file = self._filename
        # Add extension (if missed).
        ext = os.path.splitext(file)[-1]
        if not ext:
            file += VehicleLogBook._extension
        # Serialize.
        with gzip.open(file, 'wb') as fh:
            pickle.dump(self, fh, pickle.HIGHEST_PROTOCOL)
        self._modified = False
        self._filename = file

    @staticmethod
    def load(file):
        """ Create class instance from previously saved instance.

        Using pickle module.

        Warning
        -------
        The pickle module is not secure against erroneous or maliciously
        constructed data. Never unpickle data received from an untrusted or
        unauthenticated source.
        """
        # Add extension (if missed).
        ext = os.path.splitext(file)[-1]
        if not ext:
            file += VehicleLogBook._extension
        # Deserialize.
        with gzip.open(file, 'rb') as fh:
            vehice_log_book = pickle.load(fh)
        vehice_log_book._changed = False
        # Check type.
        if not isinstance(vehice_log_book, VehicleLogBook):
            raise TypeError("File {0} has unexpected type: {1}".format(
                file,
                type(vehice_log_book)))
        # Check version.
        if vehice_log_book._version != VehicleLogBook._version:
            warnings.warn("File {0} created by another version "
                          "of class <VehicleLogBook>".format(file), Warning)
        return vehice_log_book

    def __str__(self):
        return self._operations_log.__str__()


if __name__ == "__main__":
    # If running that module as the main program - do doctests.
    import doctest
    doctest.testmod()
