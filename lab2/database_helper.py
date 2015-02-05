

__author__ = 'wyz'

import sqlite3
from flask import g


DATABASE = "C:\Users\Pelle\Dropbox\Webprog TDDD97\lab2\DATABASE.db"


def connect_db():
    return sqlite3.connect("database.db")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.db = connect_db()
        db.text_factory = str
    return db


def checkUser(inputEmail):
    firstPart = inputEmail.split('@')[0]
    print firstPart
    c = get_db()
    result = c.execute("select email from users where email like 'firstPart%'")

    if result == inputEmail:
        return True
    return False


def signUpUser(email, password, firstname, familyname, gender, city, country):
    c = get_db()
    c.execute("insert into users (email, password, firstname, familyname, gender, city, country) values"
        " ('email', 'password', 'firstname', 'familyname', 'gender', 'city', 'country')" )
    c.commit()
    c.close()


#(email, password, firstname, familyname, gender, city, country)}


def checkPassword(inputEmail, password):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select password from users where email like '" + inputEmail + "'")
    pwList = [row[0] for row in cursor.fetchall()]

    if len(pwList) == 0:
        print "inget hittades"
        return False

    dbPassword = pwList[0]
    if password == dbPassword:
        return True
    else:
        return False


def signInUser(token, email):
    c = get_db()
    print "insert into loggedInUsers values ('" + token + "', '" + email + "')"
    c.execute("insert into loggedInUsers values ('" + token + "', '" + email + "')")
    c.commit()
    c.close()



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
