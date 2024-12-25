"""
Establishes a connection with the Vertica database using given credentials in a config file, cleans and initializes
a specific table, inserts data, fetches and prints the data, and asserts that the data count is correct, handling any
database and query related errors while providing debug logging.

BASIC TESTS
https://github.com/jbfavre/python-vertica/blob/master/vertica_python/tests/basic_tests.py
"""
import json
import logging

import vertica_python as vp
from vertica_python.errors import MissingSchema
from vertica_python.errors import QueryError


def init_table(cur):
    # clean old table
    cur.execute('DROP TABLE IF EXISTS sbm_covid19_workspace.vertica_python_unit_test;')

    # create test table
    cur.execute("""CREATE TABLE sbm_covid19_workspace.vertica_python_unit_test (
                    a int,
                    b varchar(32)
                    ) ;
                """)


with open("config.json") as f:
    conn_info = json.load(f)
    conn_info['log_level'] = logging.DEBUG
    conn_info['use_prepared_statements'] = True

try:
    with vp.connect(**conn_info) as conn:
        cur = conn.cursor()
        init_table(cur)

        cur.execute(""" INSERT INTO sbm_covid19_workspace.vertica_python_unit_test (a, b) VALUES (1, 'aa') """)
        cur.execute(""" INSERT INTO sbm_covid19_workspace.vertica_python_unit_test (a, b) VALUES (2, 'bb') """)
        cur.execute(""" INSERT INTO sbm_covid19_workspace.vertica_python_unit_test (a, b) VALUES (3, 'cc') """)
        conn.commit()

        cur.execute("SELECT a, b from sbm_covid19_workspace.vertica_python_unit_test ORDER BY a ASC")

        res = cur.fetchall()
        for i in res:
            print(i)

        # for row in cur.iterate():
        #     break

        # make new query and verify result
        cur.execute(""" SELECT COUNT(*) FROM sbm_covid19_workspace.vertica_python_unit_test """)
        res = cur.fetchall()
        assert 1 == len(res)
        assert 3 == res[0][0]

except ConnectionError as ce:
    print(ce)
except MissingSchema as ms:
    print(ms)
except QueryError as ce:
    print(ce)
except Exception as ex:
    print(ex)
finally:
    # conn.close()  # Nope ¯\_(ツ)_/¯
    print("Done.")

exit(0)
