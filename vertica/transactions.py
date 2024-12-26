# Connects to a Vertica database, creates a table 'mytab' in the 'my_workspace' schema, inserts some data,
# updates it, retrieves the results, and handles various exceptions, using a configuration file for connectivity settings.
import json
import logging

from vertica_python import connect
from vertica_python.errors import MissingSchema
from vertica_python.errors import QueryError


def conn():
    with open("config.json") as f:
        conn_info = json.load(f)
        conn_info['log_level'] = logging.DEBUG
        conn_info['use_prepared_statements'] = True
    con = connect(**conn_info)
    return con


def init_table(cur):
    # clean old table
    cur.execute('DROP TABLE IF EXISTS my_workspace.mytab;')
    # create test table
    cur.execute(""" CREATE TABLE my_workspace.mytab (
    id INT NOT NULL,
    firstname VARCHAR(50) NOT NULL,
    lastname VARCHAR(50) NOT NULL);   
    COMMIT; """)  # <-- Inline commit.


def insert(cur):
    """
    I think it hangs when you use BEGIN and END or COMMIT.
    Do like the following:
    """
    cur.execute("INSERT INTO my_workspace.mytab(id, firstname, lastname) VALUES (1, 'Britney', 'Spears');")
    cur.execute("UPDATE my_workspace.mytab SET id = 'Spears' WHERE lastname = 'Spears';")
    cur.execute("INSERT INTO my_workspace.mytab(id, firstname, lastname) VALUES (2, 'Zsa Zsa', 'Gabor');")
    con.commit()  # <-- DO LIKE THIS.


def check_it(cur):
    cur.execute("SELECT * FROM my_workspace.mytab;")
    res = cur.fetchall()
    print(res)


# START
try:
    con = conn()
    cur = con.cursor()
    init_table(cur)
    insert(cur)
    check_it(cur)
except ConnectionError as ce:
    print(ce)
except MissingSchema as ms:
    print(ms)
except QueryError as qe:
    print(qe)
except Exception as ex:
    print(ex)
finally:
    # conn.close()  # Nope ¯\_(ツ)_/¯
    print("Done.")

exit(0)
