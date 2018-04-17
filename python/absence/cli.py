from   argparse import ArgumentParser
import datetime
import os
import pwd

import absence.api.client
from   absence.dates import parse_date, DAY
from   absence.model import Absence

#-------------------------------------------------------------------------------

def cmd_add(client, args):
    start   = parse_date(args.start)
    end     = parse_date(args.end)
    end     = start if end is None else end
    dates   = slice(start, end + DAY)
    abc     = Absence(args.name, dates, args.code, args.notes)
    abc     = client.insert(abc)
    print(abc.id)


def cmd_show(client, args):
    abcs = list(client.search())

    start   = datetime.date.today()
    days    = 7
    for d in range(days):
        date = start + d * DAY
        date_abcs = [ a for a in abcs if a.dates.start <= date < a.dates.stop ]
        date_abcs = sorted(date_abcs, key=lambda a: a.name)
        if len(date_abcs) == 0:
            date_recs = ["(none)"]
        else:
            date_recs = [
                "{:12s} {:12s}   {}".format(
                    a.name, a.code, "" if a.notes is None else a.notes)
                for a in date_abcs
            ]

        for i, rec in enumerate(date_recs):
            print("{:10s}  {}".format(str(date) if i == 0 else "", rec))
        print()


def cmd_default(client, args):
    cmd_show(client, args)


def main():
    parser = ArgumentParser()
    cmds = parser.add_subparsers()
    parser.set_defaults(cmd=cmd_default)
    
    name = pwd.getpwuid(os.getuid()).pw_name

    cmd = cmds.add_parser("add")
    cmd.set_defaults(cmd=cmd_add)
    cmd.add_argument(
        "code", metavar="CODE", # FIXME: Choices.
        help="absence code to use")
    cmd.add_argument(
        "start", metavar="DATE", 
        help="start date")
    cmd.add_argument(
        "end", metavar="END", nargs="?", default=None,
        help="end date [def: start date]")
    cmd.add_argument(
        "--name", metavar="NAME", default=name,
        help="set absence for NAME [def: {}]".format(name))
    cmd.add_argument(
        "--notes", metavar="TEXT", default=None,
        help="additional notes")

    cmd = cmds.add_parser("show")
    cmd.set_defaults(cmd=cmd_show)

    args = parser.parse_args()

    hostname = "localhost"  # FIXME
    client = absence.api.client.Client(hostname)
    args.cmd(client, args)


if __name__ == "__main__":
    main()


