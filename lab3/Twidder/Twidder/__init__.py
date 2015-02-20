# coding=utf-8
__author__ = 'wyz'

import json
import random
import re

from flask import Flask, request, app
from gevent.wsgi import WSGIServer
from flask_sockets import Sockets
import database_helper
from geventwebsocket.handler import WebSocketHandler


app = Flask(__name__, static_url_path='')
app.debug = True
sockets = Sockets(app)

@app.route('/')
def hello():
    database_helper.init_db()
    api()
    return app.send_static_file('client.html')

"""
    Denna metod kan du strunta i sålänge, den körs aldrig ändå men kan ha kvar den ifall man behöver användning för den senare.
"""
@sockets.route('/echo')
def echo_sockets(ws):
    while True:
        message = ws.receive()
        ws.send(message)
        print "message we have sent: " +  message


"""
    ws är själva websocketen där datan strömmar från client till server. Alltså mellan client.js och __innit__.py.
    vi lägger allting vi får in i variabeln data och om den inte innehåller något printar vi "no data in socket".
    För att skicka meddelanden tillbaka till client gör vi ws.send(), och som sagt för att få data från clienten
    tar vi emot det genom ws.receive(), därmed är tvåvägskommunikationen fullbordad.

    Det verkar som att man bara kan skicka "en rad" med data åt gången. Eller snarare ett anrop från client.js mha av send() åt gången.
    Har du i client.js t.ex:
    websocket.send("första raden");
    websocket.send("andra raden");
    så kommer vår variabel data i api-metoden vara "första raden" och det skickar vi med ws.send(data) till clienten, sen efter det görs allting om
    och data blir "andra raden" och vi går sedan och skickar det med ws.send(data).
"""
@app.route('/api')
def api():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        while True:
            data = ws.receive()
            if data is None:
                print "no data in socket"
                return
            else:
                print "token: " + data
                ws.send("Data in socket: " + data)


def validEmail(email):
    if re.match("[^@]+@[^@]+\.[^@]+", email):
        return True
    return False


def validPassword(password):
    if len(password) < 4:
        return False
    return True

@app.route('/signUp', methods=["POST"])
def signUp():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        familyname = request.form['familyname']
        gender = request.form['gender']
        city = request.form['city']
        country = request.form['country']

        if not email or not password or not firstname or not familyname or not gender or not city or not country:
            return json.dumps({"success": False, "message": "Incomplete forms"})

        if not validEmail(email):
            return json.dumps({"success": False, "message": "Email not valid."})

        if not validPassword(password):
            return json.dumps({"success": False, "message": "Password must be 4 characters or more."})

        result = database_helper.signUpUser(email, password, firstname, familyname, gender, city, country)
        if result:
            return json.dumps({"success": True, "message": "Successfully created user!"})
        else:
            return json.dumps({"success": False, "message": "User already exists"})


def generateToken():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ''.join(random.choice(letters) for _ in range(len(str(letters))))
    if not database_helper.userSignedIn(token):
        return token
    else:
        print "Token already exists. Re-generating..."
        return generateToken()


@app.route('/signOut', methods=['POST'])
def signOut():
    if request.method == 'POST':
        token = request.form['token']
        email = database_helper.getEmail(token)
        if not database_helper.userExists(email):
            return json.dumps({"success": False, "message": "No such user logged in."})

        if database_helper.signOut(token):
            return json.dumps({"success": True, "message": "Successfully logged out."})
        else:
            return json.dumps({"success": False, "message": "Could not log out."})


@app.route('/changePassword', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        token = request.form['token']
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        if not validPassword(newPassword):
            return json.dumps({"success": False, "message": "Password must be 4 characters or more."})

        if database_helper.changePassword(token, oldPassword, newPassword):
            return json.dumps({"success": True, "message": "Successfully changed password."})
        else:
            return json.dumps({"success": False, "message": "Could not change password."})



@app.route('/signIn', methods=["POST"])
def signIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        if database_helper.checkPassword(email, password):
            token = generateToken()
            if database_helper.userSignedIn(token): # Denna fungerar uppenbarligen inte men här får vi kolla så inte det finns två använder inloggade på samma email.
                print "duplicate users!!!"
            database_helper.signInUser(token, email)
            return json.dumps({"success": True, "message": "Successfully signed in.", "data": token})
        else:
            return json.dumps({"success": False, "message": "Wrong username or password."})




@app.route('/postMessage', methods=["POST"])
def postMessage():
    if request.method == 'POST':
        token = request.form['token']
        content = request.form['content']
        toEmail = request.form['toEmail']

        if database_helper.userSignedIn(token):
            if database_helper.userExists(toEmail):
                if database_helper.postMessage(token, content, toEmail):
                    return json.dumps({"success": True, "message": "Message posted."})
                else:
                    return json.dumps({"success": False, "message": "Failed to post message"})
            else:
                return json.dumps({"success": False, "message": "Nu such user."})
        else:
            return json.dumps({"success": False, "message": "You are not signed in"})





@app.route('/getMessagesByToken/<token>', methods=["GET"])
def getMessagesByToken(token):
    if request.method == 'GET':
        userEmail = database_helper.getEmail(token)
        return getMessages(token, userEmail)

@app.route('/getMessagesByEmail', methods=["GET"])
def getMessagesByEmail():
    if request.method == 'GET':
        token = request.args.get('token')
        userEmail = request.args.get('email')
        return getMessages(token, userEmail)


def getMessages(token, userEmail):
    if database_helper.userSignedIn(token):
        if database_helper.userExists(userEmail):
            messages = database_helper.getMessages(userEmail)
            return json.dumps({"success": True, "message": "User messages retrieved.", "data": messages})
        else:
            return json.dumps({"success": False, "message": "Nu such user."})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})


@app.route('/getUserDataByToken/<token>', methods=["GET"])
def getUserDataByToken(token):
    if request.method == 'GET':
        userEmail = database_helper.getEmail(token)
        return getUserData(token, userEmail)

@app.route('/getUserDataByEmail', methods=["GET"])
def getUserDataByEmail():
     if request.method == 'GET':
        token = request.args.get('token')
        userEmail = request.args.get('email')
        return getUserData(token, userEmail)

def getUserData(token, userEmail):
    if database_helper.userSignedIn(token):
        if database_helper.userExists(userEmail):
            userData = database_helper.getUserData(userEmail)
            return json.dumps({"success": True, "message": "User data retrieved.", "data": userData})
        else:
            return json.dumps({"success": False, "message": "Nu such user."})
    else:
        return json.dumps({"success": False, "message": "You are not signed in."})



@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.debug = True
    http_server = WSGIServer(('', 5000), app, handler_class=WebSocketHandler)
    print "Serving on port 5000..."
    http_server.serve_forever()