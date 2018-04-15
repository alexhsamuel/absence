import argparse
import flask
import logging
from   pathlib import Path

from   ooo import DEFAULT_PORT
import ooo.api
from   ooo.db import SqliteDB

#-------------------------------------------------------------------------------

app = flask.Flask(__name__)

app.register_blueprint(ooo.api.api, url_prefix="/api/v1")

def main():
    logging.basicConfig(
        format  ="%(asctime)s [%(levelname)-7s] %(name)s: %(message)s",
        datefmt ="%Y-%m-%dT%H:%M:%S",
    )

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--host", metavar="ADDR", default="localhost",
        help="serve on ADDR [def: localhost]")
    parser.add_argument(
        "--port", metavar="PORT", type=int, default=DEFAULT_PORT,
        help="serve on PORT [def: {}]".format)
    parser.add_argument(
        "--repo", metavar="PATH", type=Path, default=Path("./repo"),
        help="use repo dir at PATH")
    parser.add_argument(
        "--initialize", action="store_true", default=False,
        help="initialize repo if missing")
    parser.add_argument(
        "--debug", action="store_true", default=False,
        help="run Werkzeug in debug mode")
    parser.add_argument(
        "--log", metavar="LEVEL", default="INFO",
        help="log at LEVEL [def: INFO]")
    parser.add_argument(
        "--db", metavar="FILE", default="./ooo.sqlite",
        help="path to database")
    parser.add_argument(
        "--create-db", action="store_true", default=False,
        help="create the database")
    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log.upper()))

    # We don't cache the database as SQLite connections are thead-specific.
    # But either create or check it up front.
    if args.create_db:
        SqliteDB.create(args.db)
    else:
        SqliteDB.open(args.db)

    app.db_path = args.db
    app.run(host=args.host, port=args.port, debug=args.debug, threaded=False)


if __name__ == "__main__":
    main()


