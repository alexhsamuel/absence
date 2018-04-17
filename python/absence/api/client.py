import requests
import urllib.parse

from   . import DEFAULT_PORT
import absence.dates
from   absence.model import Absence

#-------------------------------------------------------------------------------

# FIXME: On error, show response message.

class Client:

    def __init__(self, host, port=DEFAULT_PORT, path="/api/v1"):
        self.netloc = "{}:{:d}".format(host, port)
        self.path = str(path)


    def __make_url(self, *path, **args):
        args = { k: v for k, v in args.items() if v is not None }
        return urllib.parse.urlunparse((
            "http",
            self.netloc,
            self.path + "/" + "/".join(path),
            "",
            urllib.parse.urlencode(args),
            ""
        ))


    def insert(self, absence):
        url = self.__make_url("absence")

        jso = {
            "absence": absence.to_jso(),
        }
        response = requests.post(url, json=jso)
        response.raise_for_status()
        jso = response.json()

        return Absence.from_jso(jso["absence"])
        

    def search(self, name=None, dates=None, code=None):
        url = self.__make_url(
            "search", 
            name    =name, 
            dates   =None if dates is None else absence.dates.format_dates(dates),
            code    =code
        )

        response = requests.get(url)
        response.raise_for_status()
        jso = response.json()

        return [ Absence.from_jso(o) for o in jso["absences"] ]



