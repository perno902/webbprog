__author__ = 'wyz'

from flask import Flask, request, app
import database_helper
import json
import random
import re


app = Flask(__name__)
app.debug = True


@app.route('/')
def hello():
    database_helper.init_db()
    #database_helper.testdb()
    return "world, hello"


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
    if not database_helper.tokenExists(token):
        return token
    else:
        print "Token already exists. Re-generating..."
        return generateToken()


@app.route('/signIn', methods=["POST"])
def signIn():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        database_helper.getToken(email)
        if database_helper.checkPassword(email, password):
            token = generateToken()
            database_helper.signInUser(token, email)
            database_helper.getToken(email)
            return json.dumps({"success": True, "message": "Successfully signed in.", "data": token})
        else:
            return json.dumps({"success": False, "message": "Wrong username or password."})


@app.route('/signOut', methods=['POST'])
def signOut():
    if request.method == 'POST':
        email = request.form['email']
        if not database_helper.userExists(email):
            return json.dumps({"Success": False, "message": "No such user logged in."})

        if database_helper.signOut(database_helper.getToken(email)):
            return json.dumps({"Success": True, "message": "Successfully logged out."})
        else:
            return json.dumps({"Success": False, "message": "Could not log out."})


@app.route('/changePassword', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        inputEmail = request.form['email']
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        token = database_helper.getToken(inputEmail)
        print validPassword(newPassword)
        if not validPassword(newPassword):
            print "enter here pleaseee"
            return json.dumps({"success": False, "message": "Password must be 4 characters or more."})

        if database_helper.changePassword(token, oldPassword, newPassword):
            return json.dumps({"Success": True, "message": "Successfully changed password."})
        else:
            return json.dumps({"Success": False, "message": "Could not change password."})


@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()