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
import string
import datetime

def usage_and_exit():
    raise SystemExit(__doc__) 

def err(msg):
    raise SystemExit, "ERROR: " + msg

def convert_date(date):
    """Convert a date string into a year, month and day.

    The following formats are allowed: 'today', m/d, mm/dd, m/d/yy, mm/dd/yy,
    m/d/yyyy or mm/dd/yyyy.
    """

    if date == 'today':
        d = datetime.date.today()
        return [int(d.strftime('%Y')), int(d.strftime('%m')),
                int(d.strftime('%d'))]

    m = re.search(r'^(\d\d?)/(\d\d?)$', date)               # m/d, mm/dd
    if m:
        [month, day] = [int(x) for x in m.groups()]
        year = int(datetime.date.today().strftime('%Y'))
    else:
        m = re.search(r'^(\d\d?)/(\d\d?)/(\d\d)$', date)    # m/d/yy, mm/dd/yy
        if m:
            [month, day, year] = [int(x) for x in m.groups()]
            if year <= 70:
                year += 2000
            else:
                year += 1900
        else:
            # m/d/yyyy, mm/dd/yyyy
            m = re.search(r'^(\d\d?)/(\d\d?)/(\d{4})$', date)
            if m:
                [month, day, year] = [int(x) for x in m.groups()]
            else:
                err("`%s' is not a valid date!" % date)

    try:
        # print "debug: %10s ==> %02d/%02d/%d" % (date, month, day, year)
        datetime.date(year, month, day)
    except ValueError:
        err("`%s' is not a valid date!" % date)

    return [year, month, day]

def cal_shifted_date(yyyy, mm, dd, n):
    """Figure out what date it is after shifting `yyyy/mm/dd` by `n' days.

    `n' can be any integer number (including 0 and negative values).
    """

    d = datetime.date(yyyy, mm, dd)
    d += datetime.timedelta(n)
    return d.strftime('%m/%d/%Y')

def cal_days_diff(yyyy1, mm1, dd1, yyyy2, mm2, dd2):
    """Given two dates, calculate the number of days between them."""

    date1 = datetime.date(yyyy1, mm1, dd1)
    date2 = datetime.date(yyyy2, mm2, dd2)
    diff = repr(date2 - date1)
    g = re.search('datetime.timedelta\((.*)\)', diff)
    return int(g.groups()[0])

def parse_args(argv):
    verbose = True

    try:
        opts, args = getopt.getopt(argv, "q", ['quiet', ])
    except getopt.GetoptError:
        usage_and_exit()

    for opt, arg in opts:
        if opt in ("-q", "--quiet"):
            verbose = False

    if len(args) != 2:
	usage_and_exit()

    return verbose, args[0], args[1]

def main(argv):
    verbose, arg1, arg2 = parse_args(argv)

    [year1, month1, day1] = convert_date(arg1)
    if '/' in arg2 or arg2 == 'today':
	[year2, month2, day2] = convert_date(arg2)
        ndays = cal_days_diff(year1, month1, day1, year2, month2, day2)
        if verbose:
            print "%02d/%02d/%d to %02d/%02d/%d: %d day(s)" % \
                    (month1, day1, year1, month2, day2, year2, ndays)
        else:
            print "%d day(s)" % ndays
    else:
	try:
	    ndays = string.atoi(arg2)
	except ValueError:
	    err("`%s' is not a valid number or date!" % arg2)

        result = cal_shifted_date(year1, month1, day1, ndays)
        if verbose:
            print "%02d/%02d/%d %s %d day(s): %s" % \
                    (month1, day1, year1, ndays >= 0 and '+' or '-', abs(ndays), result)
        else:
            print result

if __name__ == "__main__":
    main(sys.argv[1:])
