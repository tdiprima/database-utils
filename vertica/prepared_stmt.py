# Loads connection settings from a JSON file, connects to a Vertica database, drops a table if it exists,
# creates a new table, and inserts predefined data into it, then commits the changes and closes the connection.
import json
import logging

import vertica_python

with open("config.json") as f:
    conn_info = json.load(f)
    conn_info['log_level'] = logging.DEBUG
    conn_info['use_prepared_statements'] = True

# Create connection
connection = vertica_python.connect(**conn_info)

# Check connection
# if connection.connect_error:
#     print("Connection failed: " + connection.connect_error)

# do things
cur = connection.cursor()

cur.execute("DROP TABLE IF EXISTS my_workspace.MyGuests;")
cur.execute(""" CREATE TABLE my_workspace.MyGuests
(
    firstname VARCHAR(30) NOT NULL,
    lastname  VARCHAR(30) NOT NULL,
    email     VARCHAR(50)
); """)

# prepare, set parameters, and execute
cur.execute("INSERT INTO my_workspace.MyGuests (firstname, lastname, email) VALUES (?, ?, ?)",
            ["John", "Doe", "john@example.com"])
cur.execute("INSERT INTO my_workspace.MyGuests (firstname, lastname, email) VALUES (?, ?, ?)",
            ["Mary", "Moe", "mary@example.com"])
cur.execute("INSERT INTO my_workspace.MyGuests (firstname, lastname, email) VALUES (?, ?, ?)",
            ["Julie", "Dooley", "julie@example.com"])
connection.commit()

print("New records created successfully")

connection.close()

exit(0)
