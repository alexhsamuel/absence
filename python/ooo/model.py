from   . import dates

#-------------------------------------------------------------------------------

class StatusError(RuntimeError):

    pass



class InvalidCodeError(StatusError):

    pass



class StatusRecord:

    def __init__(self, name, dates, code, notes):
        self.id     = None
        self.name   = name
        self.dates  = dates
        self.code   = code
        self.notes  = notes


    def __repr__(self):
        return "{}({!r}, {}:{}, {!r}, {!r})".format(
            self.__class__.__name__, self.name, self.dates.start, 
            self.dates.stop, self.code, self.notes,
        )


    def to_jso(self):
        return {
            "id"    : self.id,
            "name"  : self.name,
            "dates" : dates.dates_to_jso(self.dates),
            "code"  : self.code,
            "notes" : self.notes,
        }


    @classmethod
    def from_jso(Class, jso):
        rec = Class(
            jso["name"],
            dates.dates_from_jso(jso["dates"]),
            jso["code"],
            jso["notes"],
        )
        rec.id = jso["id"]
        return rec



