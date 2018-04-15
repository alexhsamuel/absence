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
            "dates" : {
                "start" : self.dates.start,
                "stop"  : self.dates.stop,
            },
            "status": self.status,
            "notes" : self.notes,
        }



