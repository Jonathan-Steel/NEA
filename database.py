# DO NOT EXECUTE! Code used to create the various tables within the database files.

import sqlite3

conn = sqlite3.connect("groups.db")

c = conn.cursor()

# Code used to create the user table
c.execute("""CREATE TABLE users (
            username text,
            password text,
            role text
            )""")

# Creating groups database
c.execute("""CREATE TABLE groups (
            username text,
            role text,
            lap_time integer,
            complete_time integer
            )""")

# Creating lap times table
c.execute("""CREATE TABLE times (
            username text,
            time integer,
            type text
            )""")

conn.commit()

conn.close()