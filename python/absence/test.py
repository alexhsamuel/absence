from   datetime import date

import absence.db
from   absence.model import Absence

#-------------------------------------------------------------------------------

def create_db(path):
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


