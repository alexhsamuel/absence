from   datetime import date

import ooo.db
from   ooo.model import StatusRecord

#-------------------------------------------------------------------------------

def create_db(path):
    db = ooo.db.SqliteDB.create(path)
    db.insert(StatusRecord(
        "asamuel", 
        slice(date(2018, 2, 1), date(2018, 3, 1)),
        "vacation", 
        "In Kamchatka.",
    ))
    db.insert(StatusRecord(
        "asamuel", 
        slice(date(2018, 4, 1), date(2018, 5, 11)),
        "vacation", 
        "In Antarctica.",
    ))


