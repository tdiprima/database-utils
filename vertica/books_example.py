# Connects to a Vertica database to perform and manage various operations, such as selection, insertion, deletion
# and transaction with error handling on a particular table named 'sbm_covid19_workspace.Books'.
# https://github.com/vertica/vertica-python
import logging
import sys

import vertica_python

# Write DEBUG level logs to './vertica_python.log'
conn_info = {'host': 'vert',
             'port': 5433,
             'user': 'me',
             'password': 'sweet',
             'database': 'petite',
             'log_level': logging.DEBUG}


def select1():
    cur.execute("SELECT * FROM sbm_covid19_workspace.Books")  # LIMIT 2")
    for row in cur.iterate():
        print(row)


def select_where():
    data = {'propA': 5, 'propB': 'Book5'}
    cur.execute("SELECT * FROM " + a_table + " WHERE id = :propA AND name = :propB", data)
    # converted into a SQL command similar to: "SELECT * FROM a_table WHERE a = 1 AND b = 'stringValue'"
    print(cur.fetchall())


def select_placeholders():
    cur1 = connection.cursor()
    data = (6, "Book6")
    cur1.execute("SELECT * FROM " + a_table + " WHERE id = %s AND name = %s", data)  # correct
    # converted into a SQL command similar to: "SELECT * FROM a_table WHERE a = 1 AND b = 'O''Reilly'"
    print(cur1.fetchall())


def transaction():
    # query_string = "BEGIN TRANSACTION "  # <-- Nope.
    query_string += "INSERT INTO " + a_table + " VALUES (20, 'Book15', 'Cat5', 2000) "
    query_string += "UPDATE " + a_table + " SET price = '25 Hundred' WHERE id = 20"
    query_string += "DELETE from " + a_table + " WHERE id = 20"
    # query_string += "COMMIT TRANSACTION "  # <-- Nope.
    return query_string


def insert():
    cur.execute("INSERT INTO " + a_table + " VALUES (20, 'Book15', 'Cat5', 2000); COMMIT;")
    print('inserted')


def delete():
    # Delete WILL NOT execute unless you put COMMIT.
    cur.execute("DELETE FROM " + a_table + " WHERE id = 20; COMMIT;")
    print('deleted')


def trans():
    print("trans")

    try:
        cur.execute("INSERT INTO " + a_table + " VALUES (20, 'Book15', 'Cat5', 2000)")
        print("inserted")
        # It got here, borked, and stopped. Which is good, but it didn't roll back.
        cur.execute("UPDATE " + a_table + " SET price = '25 Hundred' WHERE id = 20")
        print("updated")
        cur.execute("DELETE from " + a_table + " WHERE id = 20; COMMIT;")
        print("deleted")
    except Exception as e:
        print(e)
        print("Unexpected error:", sys.exc_info()[0])
    finally:
        print("finally")


a_table = "sbm_covid19_workspace.Books"
with vertica_python.connect(**conn_info) as connection:
    cur = connection.cursor()
    trans()

exit(0)
