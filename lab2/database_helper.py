

__author__ = 'wyz'

import sqlite3
from flask import g


DATABASE = 'database.db'


def connect_db():
    return sqlite3.connect("database.db")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.db = connect_db()
    return db


#def signUpUser(email, password, firstname, familyname, gender, city, country):
#    return


def testdb():
    c = get_db()
    c.execute("insert into users values ('test@gmail.com', 'test', 'fname', 'famname', 'male', 'link', 'sweden')")
    c.execute("insert into users values('test2@gmail.com', 'test2', 'fname', 'famname', 'male', 'link', 'sweden')")
    c.commit()
    c.close()
   # c.execute("select * from users")


def init_db():
    c = get_db()
    c.execute("drop table if exists users")
    c.execute("CREATE TABLE users(email TEXT PRIMARY KEY, password TEXT, firstname TEXT, familyname TEXT, gender TEXT, city TEXT, country TEXT)")

    c.commit()
    print "database initalized"


def close():
    get_db().close()