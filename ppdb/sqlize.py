import sqlite3
import dataset
PPDB_LEXICAL = "lexical.parse"  # The lexical ppdb rules
PPDB_O2M = "o2m.parse"  # The lexical ppdb rules
RULES_DATABASE_URI = "sqlite:///rules.db"

rules_database = dataset.connect(RULES_DATABASE_URI)
lexical_rules = rules_database["lexical"]
o2m_rules = rules_database["o2m"]

rule_columns = ("source", "target", "features")

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

parse_ppdb(PPDB_LEXICAL, lexical_rules)
parse_ppdb(PPDB_O2M, o2m_rules)

