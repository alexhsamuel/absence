from   contextlib import closing
from   datetime import date
from   pathlib import Path

import absence.db
from   absence.model import Absence

#-------------------------------------------------------------------------------

def test_create(tmpdir):
    path = Path(tmpdir) / "test_create.sqlite"
    rec = Absence(
        "asamuel", 
        slice(date(2018, 4, 9), date(2018, 4, 13)),
        "vacation", 
        "In Scotland.",
    )
    with closing(absence.db.SqliteDB.create(path)) as db:
        db.insert(rec)
    assert rec.id is not None


def test_query_dates(tmpdir):
    path = Path(tmpdir) / "test_query_dates.sqlite"
    db = absence.db.SqliteDB.create(path)
    db.insert(Absence(
        "asamuel", 
        slice(date(2018, 2, 1), date(2018, 3, 1)),
        "vacation", 
        "In Kamchatka.",
    ))
    db.insert(Absence(
        "asamuel", 
        slice(date(2018, 4, 1), date(2018, 5, 11)),
        "vacation", 
        "In Antarctica.",
    ))

    recs = list(db.search())
    assert len(recs) == 2

    recs = list(db.search(dates=slice(None, None)))
    assert len(recs) == 2

    recs = list(db.search(dates=slice(None, date(2018, 2, 2))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(None, date(2018, 3, 2))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(None, date(2018, 4, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(None, date(2019, 1, 1))))
    assert len(recs) == 2

    recs = list(db.search(dates=slice(date(2018, 2, 28), None)))
    assert len(recs) == 2

    recs = list(db.search(dates=slice(date(2018, 3, 1), None)))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 4, 1), None)))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 4, 30), None)))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 5, 1), None)))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2017, 1, 1), date(2018, 2, 1))))
    assert len(recs) == 0

    recs = list(db.search(dates=slice(date(2017, 1, 1), date(2018, 2, 2))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2017, 1, 1), date(2018, 3, 2))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2017, 1, 1), date(2018, 4, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2017, 1, 1), date(2019, 1, 1))))
    assert len(recs) == 2

    recs = list(db.search(dates=slice(date(2018, 2, 28), date(2019, 1, 1))))
    assert len(recs) == 2

    recs = list(db.search(dates=slice(date(2018, 3, 1), date(2019, 1, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 4, 1), date(2019, 1, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 4, 30), date(2019, 1, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 5, 1), date(2019, 1, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 3, 1), date(2018, 4, 1))))
    assert len(recs) == 0

    recs = list(db.search(dates=slice(date(2018, 2, 20), date(2018, 4, 1))))
    assert len(recs) == 1

    recs = list(db.search(dates=slice(date(2018, 3, 1), date(2018, 4, 10))))
    assert len(recs) == 1

    assert recs[0].notes == "In Antarctica."


