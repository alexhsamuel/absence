import datetime
import functools

#-------------------------------------------------------------------------------

def nullable(fn):
    @functools.wraps(fn)
    def wrapped(arg, *args, **kw_args):
        if arg is None:
            return None
        else:
            return fn(arg, *args, **kw_args)

    return wrapped


DAY = datetime.timedelta(1, 0, 0)

@nullable
def parse_date(date):
    return datetime.datetime.strptime(date, "%Y-%m-%d").date()


@nullable
def format_date(date):
    return date.strftime("%Y-%m-%d")


@nullable
def parse_dates(dates):
    if ":" in dates:
        start, stop = dates.split(":", 1)
        start = None if start == "" else parse_date(start)
        stop = None if stop == "" else parse_date(stop)
        return slice(start, stop)
    else:
        date = parse_date(dates)
        return slice(date, date + DAY)


@nullable
def format_dates(dates):
    return (
          "" if dates.start is None else format_date(dates.start)
        + ":"
        + "" if dates.stop is None else format_date(dates.stop)
    )


@nullable
def dates_to_jso(dates):
    return {
        "start" : format_date(dates.start),
        "stop"  : format_date(dates.stop),
    }


@nullable
def dates_from_jso(jso):
    return slice(
        parse_date(jso.get("start", None)),
        parse_date(jso.get("stop", None)),
    )


