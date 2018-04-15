from   argparse import ArgumentParser
import datetime

from   ooo.db import SqliteDB

#-------------------------------------------------------------------------------

def main():
    parser = ArgumentParser()
    parser.add_argument(
        "--db", metavar="FILE", default="./ooo.sqlite",
        help="path to database")
    parser.add_argument(
        "--create-db", action="store_true", default=False,
        help="create the database")
    args = parser.parse_args()

    db = SqliteDB.create(args.db) if args.create_db else SqliteDB.open(args.db)
    for rec in db.search():
        print(rec)


if __name__ == "__main__":
    main()


