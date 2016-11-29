import sqlite3
import dataset
PPDB_LEXICAL = "lexical.parse"  # The lexical ppdb rules
RULES_DATABASE_URI = "sqlite:///rules.db"

rules_database = dataset.connect(RULES_DATABASE_URI)
lexical_rules = rules_database["lexical"]

rule_columns = ("source", "target", "features")

with open(PPDB_LEXICAL, "r") as f:
    lines = f.readlines()
    for line in lines:
        rule = line.split("|||")
        lexical_rules.insert(
            {
                "source": rule[0].strip(),
                "target": rule[1].strip(),
                "features": rule[2].strip()
            }
        )

print("done")

