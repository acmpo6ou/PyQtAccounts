#!/usr/bin/env python3

import glob

for db in glob.glob("*.db"):
    name = db.rstrip(".db")
    salt = open(f"{name}.bin", "rb").read()
    db = open(db, "rb").read()

    with open(f"{name}.dba", "wb") as dba:
        dba.write(salt)
        dba.write(db)


