"""
Build a PPDB SQLite substitution database out of the given ppdb rules we parsed
"""

import sqlite3
import dataset
import glob
import os

RULES_DATABASE_URI = "sqlite:///ppdb/rules2.db"


def get_parsed_ppdbs():
    ppdb_files = list(glob.glob("ppdb/*.parse"))

    # return [os.path.splitext(basename(filename))[0] for filename in ppdb_files]
    return ppdb_files


def parse_ppdb(rules_file, table):
    with open(rules_file, "r") as f:
        lines = f.readlines()
        for line in lines:
            rule = line.split("|||")
            table.insert(
                {
                    "source": rule[0].strip(),
                    "target": rule[1].strip(),
                    "features": rule[2].strip()
                }
            )

        print("done with {}".format(rules_file))

def go():
    rules_database = dataset.connect(RULES_DATABASE_URI)

    ppdb_files = get_parsed_ppdbs()

    for ppdb_file in ppdb_files:
        # The type will be o2m or lexical, but can later be expanded if we need
        rules_type = os.path.splitext(os.path.basename(ppdb_file))[0]
        rules_table = rules_database[rules_type]

        parse_ppdb(ppdb_file, rules_table)

if __name__ == "__main__":
    go()
