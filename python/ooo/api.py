import datetime
import flask

from   ooo.dates import parse_dates
from   ooo.db import SqliteDB

#-------------------------------------------------------------------------------

api = flask.Blueprint("ooo", __name__)

def _get_db():
    return SqliteDB.open(flask.current_app.db_path)


@api.route("/search", methods=["GET"])
def get_search():
    name    = flask.request.args.get("name", None)
    dates   = flask.request.args.get("dates", None)
    status  = flask.request.args.get("status", None)

    dates   = slice(None, None) if dates is None else parse_dates(dates)

    recs = _get_db().search(name=name, dates=dates, status=status)
    return flask.jsonify({
        "results": [ r.to_jso() for r in recs ],
    })



