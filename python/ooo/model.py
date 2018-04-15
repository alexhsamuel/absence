from   . import dates

#-------------------------------------------------------------------------------

class StatusRecord:

    def __init__(self, name, dates, status, notes):
        self.id     = None
        self.name   = name
        self.dates  = dates
        self.status = status
        self.notes  = notes


    def __repr__(self):
        return "{}({!r}, {}:{}, {!r}, {!r})".format(
            self.__class__.__name__, self.name, self.dates.start, 
            self.dates.stop, self.status, self.notes,
        )


    def to_jso(self):
        return {
            "id"    : self.id,
            "name"  : self.name,
            "dates" : dates.dates_to_jso(self.dates),
            "status": self.status,
            "notes" : self.notes,
        }


    @classmethod
    def from_jso(Class, jso):
        rec = Class(
            jso["name"],
            dates.dates_from_jso(jso["dates"]),
            jso["status"],
            jso["notes"],
        )
        rec.id = jso["id"]
        return rec



