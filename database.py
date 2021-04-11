import sqlite3

conn = sqlite3.connect("users.db")

c = conn.cursor()

# Code used to create the user table
# c.execute("""CREATE TABLE users (
#             username text,
#             password text
#             )""")

# c.execute("INSERT INTO users VALUES ('Jonathan', 'password')")

# c.execute("INSERT INTO users VALUES (:username, :password)", {'username': 'Jonaldinho', 'password': 'password'})

c.execute("SELECT * FROM users WHERE password=:password", {'password': 'password'})

print(c.fetchall())

conn.commit()

conn.close()