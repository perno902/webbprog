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



def userExists(inputEmail):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select email from users where email like ?", (inputEmail,))
    userInfo = [row[0] for row in cursor.fetchall()]
    if len(userInfo) == 0:
        return False
    else:
        return True

def userSignedIn(token):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select email from loggedInUsers where token like ?", (token,))
    userInfo = [row[0] for row in cursor.fetchall()]
    if len(userInfo) == 0:
        return False
    else:
        return True


def getToken(inputEmail):
    c = get_db()
    cursor = c.cursor()
    try:
        cursor.execute("select * from loggedInUsers where email like ?", (inputEmail,))
        userToken = [row[0] for row in cursor.fetchall()]
        if len(userToken) != 0:
            return userToken[0]
        else:
            print "No token with that email logged in."
    except ValueError:
        print "Something is off."

def getToken(token):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select email from loggedInUsers where token like ?", (token,))
    email = [row[0] for row in cursor.fetchall()][0]
    return email

def getMessages(userEmail):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select writer, message from messages where recipient like ?", (userEmail,))

    firstElement = True
    messageObj = "["
    for row in cursor:
        if not firstElement:
            messageObj += ", "
        else:
            firstElement = False
        messageObj += "{writer: " + row[0] + ", content: " + row[1] + "}"
    messageObj += "]"

    return messageObj


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
