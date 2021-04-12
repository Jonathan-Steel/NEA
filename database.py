import sqlite3

conn = sqlite3.connect("groups.db")

c = conn.cursor()

# Code used to create the user table
# c.execute("""CREATE TABLE users (
#             username text,
#             password text,
#             role text
#             )""")

# Creating groups database
c.execute("DROP TABLE groups")

c.execute("""CREATE TABLE groups (
            username text,
            role text,
            lap_time integer,
            complete_time integer
            )""")

# Creating lap times table
# c.execute("""CREATE TABLE times (
#             username text,
#             time integer,
#             type text
#             )""")

# # c.execute("INSERT INTO users VALUES ('Jonathan', 'password')")

# # c.execute("INSERT INTO users VALUES (:username, :password)", {'username': 'Jonaldinho', 'password': 'password'})

# c.execute("SELECT * FROM users WHERE password=:password", {'password': 'password'})

# print(c.fetchall())

conn.commit()

conn.close()