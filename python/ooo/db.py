from   contextlib import closing
from   pathlib import Path
import sqlite3

from   .model import StatusRecord

#-------------------------------------------------------------------------------

class SqliteDB:

    def __init__(self, conn):
        self.__conn = conn


    def close(self):
        self.__conn.close()
        self.__conn = None


    @classmethod
    def create(cls, path):
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
                    status      TEXT NOT NULL,
                    notes       TEXT
                )
            """)

        return cls.open(path)


    @classmethod
    def open(cls, path):
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        conn = sqlite3.connect(str(path), detect_types=True)
        return cls(conn)


    def insert(self, status):
        with closing(self.__conn.cursor()) as cursor:
            cursor.execute(
                "INSERT INTO status VALUES (?, ?, ?, ?, ?, ?)",
                 (
                     False,
                     status.name,
                     status.dates.start,
                     status.dates.stop,
                     status.status,
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


    def search(self, name=None, dates=None, status=None):
        conditions = ["NOT DELETED"]
        parameters = []
        if name is not None:
            conditions.append("NAME = ?")
            parameters.append(name)
        if dates is None:
            dates = slice(None, None)
        if dates.start is not None:
            conditions.append("(dates_stop IS NULL OR dates_stop > ?)")
            parameters.append(dates.start)
        if dates.stop is not None:
            conditions.append("(dates_start IS NULL or dates_start < ?)")
            parameters.append(dates.stop)
        sql = "SELECT rowid, * FROM status WHERE " + " AND ".join(conditions)
        print(sql, parameters)

        with closing(self.__conn.cursor()) as cursor:
            cursor.execute(sql, parameters)
            for id, _, name, dates_start, dates_end, status, notes in cursor:
                rec = StatusRecord(
                    name, slice(dates_start, dates_end), status, notes)
                rec.id = id
                yield rec



