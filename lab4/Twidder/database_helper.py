#-*- coding: utf-8 -*-

__author__ = 'wyz'

import sqlite3
from flask import g
import json



#DATABASE = "C:\Users\Pelle\Documents\Skola\TDDD97\webbprog\lab3\Twidder\Twidder\DATABASE.db"
DATABASE = "C:\Users\cake\Desktop\webprog\webbprog\lab4\Twidder\DATABASE.db"


def connect_db():
    return sqlite3.connect(DATABASE)


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


def signInUser(token, email):
    c = get_db()
    try:
        c.execute("delete from loggedInUsers where email = '" + email + "'")
        c.execute("insert into loggedInUsers values (?, ?)", (token, email))
        c.commit()
    except:
        c.rollback()


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


def getEmail(token):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select email from loggedInUsers where token like ?", (token,))
    email = [row[0] for row in cursor.fetchall()]
    if len(email) == 0:
        return None
    else:
        return email[0]


def getMessages(userEmail):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select writer, message from messages where recipient like ?", (userEmail,))

    messageObj = []
    for row in cursor:
        messageObj.append({"writer": row[0], "content": row[1]})
    return json.dumps(messageObj)


def getUserData(userEmail):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select * from users where email like ?", (userEmail,))

    for row in cursor:
        dataObj = json.dumps ({"email": row[0], "firstname": row[2] ,"familyname": row[3], "gender": row[4], "city": row[5], "country": row[6]})
    return dataObj


def incrementViews(email):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("update users set viewCounter = viewCounter +1 where email like ?", (email,))
    c.commit()


def getViewCounter(email):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select viewCounter from users where email like ?", (email,))
    counter = [row[0] for row in cursor.fetchall()]
    if len(counter) == 0:
        return None
    else:
        return counter[0]



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


def checkPassword(inputEmail, password):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select password from users where email like ?", (inputEmail,))
    pwList = [row[0] for row in cursor.fetchall()]

    if len(pwList) == 0:
        return False

    dbPassword = pwList[0]
    if password == dbPassword:
        return True
    else:
        return False


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


def signOut(token):
    c = get_db()
    cursor = c.cursor()
    try:
        if len(token) != 0:
            cursor.execute("delete from loggedInUsers where token like ?", (token,))
            c.commit()
            return True
    except:
            c.rollback()
            return False


def usersLoggedIn():
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select count(*) from loggedInUsers")
    result = [row[0] for row in cursor.fetchall()][0]
    return result


def changePassword(token, oldPassword, newPassword):
    c = get_db()
    cursor = c.cursor()
    cursor.execute("select email from loggedInUsers where token like ?", (token,))
    userEmail = [row[0] for row in cursor.fetchall()]

    if not userEmail:
        return False
    if checkPassword(userEmail[0], oldPassword):
        try:
            cursor.execute("update users set password = ? where email like ?", (newPassword, userEmail[0]),)
            c.commit()
            return True
        except:
            return False
    else:
        return False


def init_db():
    c = get_db()
    c.execute("drop table if exists users")
    c.execute("CREATE TABLE users(email TEXT PRIMARY KEY, password TEXT, firstname TEXT, familyname TEXT, gender TEXT, city TEXT, country TEXT, viewcounter INTEGER)")
    c.execute("drop table if exists loggedInUsers")

    c.execute("CREATE TABLE loggedInUsers(token text primary key, email text, foreign key(email) references users(email))")
    c.execute("drop table if exists messages")
    c.execute("CREATE TABLE messages(recipient TEXT, writer TEXT, message TEXT, foreign key(recipient) references users(email), foreign key(writer) references users(email))")


    # Rows for testing purposes only:
    c.execute("insert into users values ('test@gmail.com', 'test', 'fname', 'famname', 'male', 'link', 'sweden', 3)")
    c.execute("insert into users values ('test2@gmail.com', 'test2', 'fname2', 'famname2', 'male', 'norrk', 'norway', 0)")
    #c.execute("insert into loggedInUsers values ('DGk6eSkYXk4OwckycafJrkhVvh3OtcNPVoZUYIbBV4HGgClZadrsWCAont39Zb', 'test@gmail.com')")

    c.commit()



def close():
    get_db().close()
