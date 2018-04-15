import requests
import urllib.parse

from   ooo import DEFAULT_PORT
import ooo.dates
from   ooo.model import StatusRecord

#-------------------------------------------------------------------------------

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


    def search(self, name=None, dates=None, status=None):
        url = self.__make_url(
            "search", 
            name    =name, 
            dates   =None if dates is None else ooo.dates.format_dates(dates),
            status  =status
        )

        response = requests.get(url)
        response.raise_for_status()
        jso = response.json()

        return [ StatusRecord.from_jso(o) for o in jso["results"] ]



