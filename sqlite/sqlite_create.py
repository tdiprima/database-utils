# Creates a SQLite database with tables 'person' and 'address', populates them with sample data, selects and prints
# all records from both tables, then drops the tables, and finally closes the database connection.
import sqlite3


def create():
    c.execute('''
              CREATE TABLE person
              (id INTEGER PRIMARY KEY ASC, name varchar(250) NOT NULL)
              ''')
    c.execute('''
              CREATE TABLE address
              (id INTEGER PRIMARY KEY ASC, street_name varchar(250), street_number varchar(250),
               post_code varchar(250) NOT NULL, person_id INTEGER NOT NULL,
               FOREIGN KEY(person_id) REFERENCES person(id))
              ''')

    c.execute('''
              INSERT INTO person VALUES(1, 'pythoncentral')
              ''')
    c.execute('''
              INSERT INTO address VALUES(1, 'python road', '1', '00000', 1)
              ''')

    conn.commit()


conn = sqlite3.connect('example.db')
# conn = sqlite3.connect('sqlalchemy_example.db')

c = conn.cursor()


def select():
    print('select')
    c.execute('SELECT * FROM person')
    print(c.fetchall())
    c.execute('SELECT * FROM address')
    print(c.fetchall())


def drop_it():
    print('drop_it')
    c.execute('DROP TABLE person')
    c.execute('DROP TABLE address')


select()
conn.close()

exit(0)
