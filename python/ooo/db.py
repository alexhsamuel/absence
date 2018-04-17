from   contextlib import closing
from   pathlib import Path
import sqlite3

from   .model import StatusRecord, InvalidCodeError

#-------------------------------------------------------------------------------

DEFAULT_CODES = {
    "vacation",
    "remote",
    "medical",
    "personal",
}


class SqliteDB:

    def __init__(self, conn):
        self.__conn = conn

        with closing(self.__conn.cursor()) as cursor:
            cursor.execute("SELECT code FROM codes")
            self.__codes = { c for c, in cursor }


    def close(self):
        self.__conn.close()
        self.__conn = None


    @property
    def codes(self):
        return self.__codes


    @classmethod
    def create(cls, path, codes=DEFAULT_CODES):
        path = Path(path)
        # FIXME: Race.
        if path.exists():
            raise FileExistsError(path)
        with sqlite3.connect(str(path)) as conn:
            conn.execute("""
                CREATE TABLE status (
                    deleted     BOOL NOT NULL,
                    name        TEXT NOT NULL,
                    dates_start DATE,
                    dates_stop  DATE,
                    code        TEXT NOT NULL,
                    notes       TEXT
                )
            """)
            conn.execute("""
                CREATE TABLE codes (
                    code        TEXT
                )
            """)
            conn.executemany(
                "INSERT INTO codes VALUES (?)",
                [ (s, ) for s in codes ]
            )
            conn.commit()

        return cls.open(path)


    @classmethod
    def open(cls, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        conn = sqlite3.connect(str(path), detect_types=True)

        return cls(conn)


    def insert(self, status):
        if status.code not in self.codes:
            raise InvalidCodeError("invalid code: {}".format(status.code))

        with closing(self.__conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)",
                 (
                     False,
                     status.name,
                     status.dates.start,
                     status.dates.stop,
                     status.code,
                     status.notes,
                 )
            )
            status.id = cursor.lastrowid
        self.__conn.commit()
        return status


    def delete(self, id):
        with closing(self.__conn.cursor()) as cursor:
            cursor.execute(
                "SELECT COUNT(*) FROM status WHERE NOT deleted AND rowid = ?", 
                (id, ))
            (count, ), = cursor
            if count == 0:
                raise ValueError("no id: {}".format(id))
            assert count == 1

            cursor.execute(
                "UPDATE status SET deleted = true WHERE rowid = ?", (id, ))


    def search(self, name=None, dates=None, code=None):
        conditions = ["NOT DELETED"]
        parameters = []
        if name is not None:
            conditions.append("name = ?")
            parameters.append(name)
        if dates is None:
            dates = slice(None, None)
        if dates.start is not None:
            conditions.append("(dates_stop IS NULL OR dates_stop > ?)")
            parameters.append(dates.start)
        if dates.stop is not None:
            conditions.append("(dates_start IS NULL or dates_start < ?)")
            parameters.append(dates.stop)
        if code is not None:
            conditions.append("code = ?")
            parameters.append(code)
        sql = "SELECT rowid, * FROM status WHERE " + " AND ".join(conditions)
        print(sql, parameters)

        with closing(self.__conn.cursor()) as cursor:
            cursor.execute(sql, parameters)
            for id, _, name, dates_start, dates_end, code, notes in cursor:
                rec = StatusRecord(
                    name, slice(dates_start, dates_end), code, notes)
                rec.id = id
                yield rec



