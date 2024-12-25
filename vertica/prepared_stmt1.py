# Connects to a Vertica database, creates a table, inserts multiple records, makes select queries and finally
# closes the connection. It also handles connection exceptions and ensures connection closure after execution.
import json
import logging

import vertica_python

a_table = "filename.tbl"

# Enable using server-side prepared statements at connection level
# logging.INFO, logging.WARNING
with open("config.json") as f:
    conn_info = json.load(f)
    conn_info['log_level'] = logging.DEBUG
    conn_info['use_prepared_statements'] = True

# using with for auto connection closing after usage
with vertica_python.connect(**conn_info) as connection:
    cur = connection.cursor()
    # clean old table
    cur.execute("DROP TABLE IF EXISTS " + a_table + ";")
    # create test table
    cur.execute("CREATE TABLE " + a_table + " (a INT, b VARCHAR)")
    # insert records
    cur.execute("INSERT INTO " + a_table + " VALUES (?, ?)", [1, 'aa'])
    cur.execute("INSERT INTO " + a_table + " VALUES (?, ?)", [2, 'bb'])
    cur.executemany("INSERT INTO " + a_table + " VALUES (?, ?)", [(3, 'foo'), (4, 'xx'), (5, 'bar')])
    cur.execute("COMMIT")
    cur.execute("SELECT * FROM " + a_table + " ORDER BY a")
    cur.execute("SELECT * FROM " + a_table + " WHERE a>=? AND a<=? ORDER BY a", (2, 4))
    my_list = cur.fetchall()
    print(my_list)

try:
    cerrado = connection.closed()
    if cerrado:
        print('cerrado')
    else:
        connection.close()
except Exception as ex:
    # ¯\_(ツ)_/¯
    print(ex)

exit(0)
