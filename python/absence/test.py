from   datetime import date
import random
import string

from   absence.dates import DAY
from   absence.model import Absence

#-------------------------------------------------------------------------------

NAMES = (
    "asamuel", "rblankenhorn", "ggundersen", "awhitney", "dlovell", "jgoodman", 
    "jpowers", "schuah", "fjanoos", "awestbrook", "claventhal", "ggrigorov",
)

CODES = ("vacation", "remote", "medical", "personal", )

def word():
    return "".join( 
        random.choice(string.ascii_lowercase) 
        for _ in range(random.randint(2, 10))
    )


def populate(db):
    for i in range(random.randint(10, 30)):
        start = date(2018, 1, 1) + random.randint(0, 365) * DAY
        if random.random() < 0.5:
            dates = slice(start, start + DAY)
        else:
            dates = slice(start, start + random.randint(1, 14) * DAY)
        if random.random() < 0.5:
            notes = None
        else:
            notes = " ".join( word() for _ in range(random.randint(2, 8)) )
            notes = notes.capitalize() + "."
        
        db.insert(Absence(
            random.choice(NAMES),
            dates,
            random.choice(CODES),
            notes,
        ))


