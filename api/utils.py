import re
import subprocess

import math
from datetime import datetime
from dateutil import parser
from dateutil.parser import parse

MULTIPLES = ["B", "k{}B", "M{}B", "G{}B", "T{}B", "P{}B", "E{}B", "Z{}B", "Y{}B"]


class ParserInfo(parser.parserinfo):
    WEEKDAYS = [('Mo.', 'Montag', 'Mon', 'Monday'),
                ('Di.', 'Dienstag', 'Tue', 'Tuesday'),
                ('Mi.', 'Mittwoch', 'Wed', 'Wednesday'),
                ('Do.', 'Donnerstag', 'Thu', 'Thursday'),
                ('Fr.', 'Freitag', 'Fri', 'Friday'),
                ('Sa.', 'Samstag', 'Sat', 'Saturday'),
                ('So.', 'Sonntag', 'Sun', 'Sunday')]

    MONTHS = [('Jan', 'January', 'Januar'),
              ('Feb', 'February', 'Februar'),
              ('Mar', 'March', 'Mär', 'März'),
              ('Apr', 'April'),
              ('May', 'May', 'Mai'),
              ('Jun', 'June', 'Juni'),
              ('Jul', 'July', 'Juli'),
              ('Aug', 'August'),
              ('Sep', 'Sept', 'September'),
              ('Oct', 'October', 'Okt', 'Oktober'),
              ('Nov', 'November'),
              ('Dec', 'December', 'Dez', 'Dezember')]


def hsize(i, binary=False, precision=2):
    """
    Converts number of bytes into a human readable format.

    Function adopted from from https://stackoverflow.com/a/54131913/5494186
    """
    base = 1024 if binary else 1000
    multiple = math.trunc(math.log2(i) / math.log2(base))
    value = i / math.pow(base, multiple)
    suffix = MULTIPLES[multiple].format("i" if binary else "")
    return f"{value:.{precision}f} {suffix}"


def find_dates(content, lower_bound=None, upper_bound=None):
    """
    >>> find_dates('09.2017')
    [datetime.datetime(2017, 9, 1, 0, 0)]
    >>> find_dates('31. Juli 2018')
    [datetime.datetime(2018, 7, 31, 0, 0)]
    >>> find_dates('März 2018')
    [datetime.datetime(2018, 3, 1, 0, 0)]
    >>> find_dates('08. November 2017')
    [datetime.datetime(2017, 11, 8, 0, 0)]
    >>> find_dates('Ebikon, den 05.10.2018')
    [datetime.datetime(2018, 10, 5, 0, 0)]
    >>> find_dates('vom 01.02. bis 31.03.2018')
    [datetime.datetime(2018, 2, 1, 0, 0), datetime.datetime(2018, 3, 31, 0, 0)]
    >>> find_dates('Meldung vom 06.11.17')
    [datetime.datetime(2017, 11, 6, 0, 0)]
    """
    upper_bound = upper_bound or datetime.now()
    lower_bound = lower_bound or datetime(2000, 1, 1)
    parser_info = ParserInfo()

    dates = set()
    for line in content.split('\n'):
        re_city = re.search(r'\w*,\s*(?:den)?\s*(\d.*)', line)
        if re_city:
            line = re_city.groups()[0]

        re_range = re.search(r'.*?([\d.]*)\s*(?:bis)\s*([\d.]*)', line)
        if re_range:
            line = re_range.groups()[0] \
                   + re_range.groups()[1][-4:] \
                   + ' ' \
                   + re_range.groups()[1]

        re_of = re.search(r'.*(?:vom)\s*(\d.*)', line)
        if re_of:
            line = re_of.groups()[0]

        try:
            month_year_pair = datetime.strptime(line, '%m.%Y').date()
            dates.add(datetime.combine(month_year_pair, datetime.min.time()))
        except:
            pass

        try:
            dates.add(parse(line, parser_info, dayfirst=True, default=datetime.min))
        except:
            pass

        for word in line.split(' '):
            if re.match(r'\d{4}', word):
                continue
            try:
                dates.add(parse(word, parser_info, dayfirst=True, default=datetime.min))
            except:
                pass

    return sorted([d for d in dates if lower_bound < d < upper_bound])


def check_run(cmd):
    pipes = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = pipes.communicate()
    if pipes.returncode:
        raise Exception(stderr.decode('utf-8'))
    return stdout
