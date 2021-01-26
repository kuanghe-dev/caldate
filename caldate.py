#!/usr/bin/env python

"""\
caldate - Calculate dates

Usage:
    # Calculate the number of days between `date1' and `date2'
    caldate [-q] date1 date2

    # Calculate the date of `date1' +/- number of days
    caldate [-q] date1 [+|-]num

OPTION:
    -q      quiet mode (output as little as possible)

NOTE: Dates should be `today' or in the form of m/d, mm/dd (both assuming
    current year), m/d/yy, mm/dd/yy, m/d/yyyy or mm/dd/yyyy.

Examples:
    $ caldate 08/20/2005 06/22/10
    08/20/2005 to 06/22/2010: 1767 day(s)

    $ caldate 2/1 28
    02/01/2013 + 28 day(s): 03/01/2013

    $ caldate today 12/25
    02/04/2013 to 12/25/2013: 324 day(s)
"""

import re
import sys
import getopt
import datetime

class DateError(Exception):
    pass

def usage_and_exit():
    raise SystemExit(__doc__) 

def err(msg):
    raise SystemExit("ERROR: " + msg)

class Date:
    def __init__(self, date):
        if isinstance(date, (datetime.date, datetime.datetime)):
            self._date = datetime.date(date.year, date.month, date.day)
        else:
            self._date = self.parse_date(date)

    def parse_date(self, date_str):
        if date_str == 'today':
            today = datetime.date.today()
            return datetime.date(today.year, today.month, today.day)

        m = re.search(r'^(\d\d?)/(\d\d?)$', date_str)               # m/d, mm/dd
        if m:
            [month, day] = [int(x) for x in m.groups()]
            year = datetime.date.today().year
        else:
            m = re.search(r'^(\d\d?)/(\d\d?)/(\d\d)$', date_str)    # m/d/yy, mm/dd/yy
            if m:
                month, day, year = [int(x) for x in m.groups()]
                if year < 70:
                    year += 2000
                else:
                    year += 1900
            else:
                # m/d/yyyy, mm/dd/yyyy
                m = re.search(r'^(\d\d?)/(\d\d?)/(\d{4})$', date_str)
                if m:
                    [month, day, year] = [int(x) for x in m.groups()]
                else:
                    raise DateError("'%s' is not a valid date" % date_str)

        try:
            result = datetime.date(year, month, day)
        except ValueError:
            raise DateError("'%s' is not a valid date" % date_str)

        return result

    def date(self):
        return self._date

    def __add__(self, other):
        if not isinstance(other, int):
            raise DateError("'%s' needs to be an integer" % other)

        return Date(self._date + datetime.timedelta(days=other))

    def __sub__(self, other):
        if not isinstance(other, Date):
            raise DateError("'%s' needs to be a Date instance" % other)

        return (self.date() - other.date()).days

    def __eq__(self, other):
        if not isinstance(other, Date):
            raise DateError("'%s' needs to be a Date instance" % other)

        return self._date == other.date()

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self._date.strftime('%m/%d/%Y')

def parse_args(argv):
    def parse_args_impl(argv):
        try:
            opts, args = getopt.getopt(argv, "q", ['quiet', ])
        except getopt.GetoptError:
            usage_and_exit()

        if len(args) != 2:
            usage_and_exit()

        return opts, args

    def str2date(date_str):
        try:
            result = Date(date_str)
        except DateError as e:
            err(str(e))

        return result

    def is_date(date_str):
        return '/' in date_str or date_str == 'today'

    def str2int(num_str):
        try:
            result = int(num_str)
        except ValueError:
            err("'%s' is not a valid number or date!" % args[1])

        return result

    opts, args = parse_args_impl(argv)

    verbose = True
    for opt, _ in opts:
        if opt in ("-q", "--quiet"):
            verbose = False

    date1 = str2date(args[0])

    if is_date(args[1]):
        arg2 = str2date(args[1])
    else:
        arg2 = str2int(args[1])

    return date1, arg2, verbose

def diff_dates(date1, date2, verbose=True):
    ndays = date2 - date1

    if verbose:
        print('%s to %s: %d day(s)' % (date1, date2, ndays))
    else:
        print(ndays)

    return ndays

def shift_date(date1, ndays, verbose=True):
    new_date = date1 + ndays

    if verbose:
        print("%s %s %d day(s): %s" % (
            date1, '+' if ndays >= 0 else '-', abs(ndays), new_date))
    else:
        print('%s' % new_date)

    return new_date

def main(argv):
    arg1, arg2, verbose = parse_args(argv)

    if isinstance(arg2, Date):
        diff_dates(arg1, arg2, verbose)
    else:
        shift_date(arg1, arg2, verbose)

if __name__ == "__main__":
    main(sys.argv[1:])
