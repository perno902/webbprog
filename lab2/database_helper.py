#-*- coding: utf-8 -*-

__author__ = 'wyz'

import sqlite3
from flask import g


DATABASE = "C:\Users\Pelle\Documents\Skola\TDDD97\webbprog\lab2database.db"


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
    c.execute("insert into loggedInUsers values (?, ?)", (token, email))
    c.commit()



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


def postMessage(token, content, toEmail):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("SELECT email FROM loggedInUsers WHERE token like ?", (token,))
    fromEmail = [row[0] for row in cursor.fetchall()][0]

    print fromEmail

    try:
        c.execute("INSERT INTO messages values(?, ?, ?)", (toEmail, fromEmail, content))
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

    c.execute("CREATE TABLE loggedInUsers(token text primary key, email text, foreign key(email) references users(email))")
    c.execute("drop table if exists messages")
    c.execute("CREATE TABLE messages(recipient TEXT, writer TEXT, message TEXT, foreign key(recipient) references users(email), foreign key(writer) references users(email))")


    # Row for testing purposes only:
    c.execute("insert into users values ('test@gmail.com', 'test', 'fname', 'famname', 'male', 'link', 'sweden')")

    c.commit()
    print "database initialized"



def close():
    get_db().close()
