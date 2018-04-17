import datetime
import flask

from   ..dates import parse_dates
from   ..db import SqliteDB
from   ..model import StatusRecord, StatusError

#-------------------------------------------------------------------------------

API = flask.Blueprint("ooo", __name__)

def _get_db():
    return SqliteDB.open(flask.current_app.db_path)


def _error(message, status):
    message = str(message)
    status = int(status)
    return flask.jsonify({
        "status": status,
        "message": message,
    }), status


@API.route("/status", methods=["POST"])
def post_status():
    jso = flask.request.json
    status = StatusRecord.from_jso(jso["status"])
    try:
        status = _get_db().insert(status)
    except StatusError as exc:
        return _error(exc, 400)
    return flask.jsonify({
        "absence": status.to_jso(),
    })


@API.route("/search", methods=["GET"])
def get_search():
    name    = flask.request.args.get("name", None)
    dates   = flask.request.args.get("dates", None)
    code    = flask.request.args.get("code", None)

    dates   = slice(None, None) if dates is None else parse_dates(dates)

    recs = _get_db().search(name=name, dates=dates, code=code)
    return flask.jsonify({
        "absences": [ r.to_jso() for r in recs ],
    })


