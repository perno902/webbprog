#-*- coding: utf-8 -*-

__author__ = 'wyz'

import sqlite3
from flask import g


DATABASE = "C:\Users\wyz\Dropbox\TDDD97\lab2\database.db"


def connect_db():
    return sqlite3.connect("database.db")


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g.db = connect_db()
    return db


def signUpUser(email, password, firstname, familyname, gender, city, country):
    c = get_db()
    row = (email, password, firstname, familyname, gender, city, country)
    try:
        c.execute("insert into users values(?,?,?,?,?,?,?)", row)
        c.commit()
        return True
    except:
        c.rollback()
        return False


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
    try:
        c.execute("insert into loggedInUsers values ('" + token + "', '" + email + "')")
    except:
        return False
    c.commit()
    c.close()


def getUser(inputEmail):
    c = get_db()
    cursor = c.cursor()
    user = cursor.execute("select email from loggedInUsers where email like '" + inputEmail + "'")
    userInfo = [row[0] for row in cursor.fetchall()]
    return userInfo


def getToken(inputEmail):
    c = get_db()
    cursor = c.cursor()
    token = cursor.execute("select token from loggedInUsers where email like '" + inputEmail + "'")
    return token


def signOut(inputEmail):
    c = get_db()
    cursor = c.cursor()

    try:
        cursor.execute("delete from loggedInUsers where email like '" + inputEmail + "%'")
        c.commit()
        return True
    except:
        c.rollback()
        return False


"""
def testdb():
    c = get_db()
    c.execute("insert into users values ('test@gmail.com', 'test', 'fname', 'famname', 'male', 'link', 'sweden')")
    c.execute("insert into users values('test2@gmail.com', 'test2', 'fname', 'famname', 'male', 'link', 'sweden')")
    c.commit()
    c.close()
   # c.execute("select * from users")

"""

def init_db():
    c = get_db()
    c.execute("drop table if exists users")
    c.execute("CREATE TABLE users(email TEXT PRIMARY KEY, password TEXT, firstname TEXT, familyname TEXT, gender TEXT, city TEXT, country TEXT)")
    c.execute("drop table if exists loggedInUsers")
    c.execute("CREATE TABLE loggedInUsers(token TEXT, email text PRIMARY KEY , FOREIGN KEY(email) REFERENCES users(email))")
    c.commit()
    print "database initialized"


def close():
    get_db().close()