from   argparse import ArgumentParser
import datetime

import ooo.client

#-------------------------------------------------------------------------------

def main():
    parser = ArgumentParser()
    args = parser.parse_args()
    hostname = "localhost"  # FIXME

    client = ooo.client.Client(hostname)
    for rec in client.search():
        print(rec)


if __name__ == "__main__":
    main()


