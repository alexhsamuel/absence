from   argparse import ArgumentParser
import datetime
import os
import pwd

import ooo.api.client
from   ooo.dates import parse_date, DAY
from   ooo.model import StatusRecord

#-------------------------------------------------------------------------------

def cmd_add(client, args):
    start = parse_date(args.start)
    end = parse_date(args.end)
    end = start if end is None else end
    status = StatusRecord(
        args.name, slice(start, end + DAY), args.status, args.notes)
    status = client.insert(status)
    print(status.id)


def cmd_show(client, args):
    for rec in client.search():
        print(rec)


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
        "status", metavar="STATUS", # FIXME: Choices.
        help="status to set")
    cmd.add_argument(
        "start", metavar="DATE", 
        help="start date")
    cmd.add_argument(
        "end", metavar="END", nargs="?", default=None,
        help="end date [def: start date]")
    cmd.add_argument(
        "--name", metavar="NAME", default=name,
        help="set status for NAME [def: {}]".format(name))
    cmd.add_argument(
        "--notes", metavar="TEXT", default=None,
        help="additional notes")

    cmd = cmds.add_parser("show")
    cmd.set_defaults(cmd=cmd_show)

    args = parser.parse_args()

    hostname = "localhost"  # FIXME
    client = ooo.api.client.Client(hostname)
    args.cmd(client, args)


if __name__ == "__main__":
    main()


