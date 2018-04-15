import datetime

#-------------------------------------------------------------------------------

DAY = datetime.timedelta(1, 0, 0)

def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


def parse_dates(dates):
    if ":" in dates:
        start, stop = dates.split(":", 1)
        start = None if start == "" else parse_date(start)
        stop = None if stop == "" else parse_date(stop)
        return slice(start, stop)
    else:
        date = parse_date(dates)
        return slice(date, date + DAY)


