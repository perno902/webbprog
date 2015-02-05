__author__ = 'wyz'

from flask import Flask, request, app
import database_helper
import json
import random


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    database_helper.init_db()
    #signUp()
    database_helper.testdb()

    return "world, hello"


def userExist(email):
    return database_helper.checkUser(email)


#<email>/<password>/<firstname>/<familyname>/<gender>/<city>/<country>'
@app.route('/signUp', methods=["POST"])
def signUp():
    if request.method == 'POST':
        email = request.form['email']
        if not userExist(email):
            password = request.form['password']
            firstname = request.form['firstname']
            familyname = request.form['familyname']
            gender = request.form['gender']
            city = request.form['city']
            country = request.form['country']

            result = database_helper.signUpUser(email, password, firstname, familyname, gender, city, country)

        if result:
            return json.dumps({"success": True, "message": "Successfully created user!"})
        else:
            return json.dumps({"success": False, "message": "Form incomplete"})
    else:
        return json.dumps({"success": False, "message": "User already exists"})


#email, password, firstname, familyname, gender, city, country

@app.route('/signIn', methods=["POST"])
def signIn():
    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        if database_helper.checkPassword(email, password):
            token = generateToken()
            database_helper.signInUser(token, email)
            return json.dumps({"success": True, "message": "Successfully signed in.", "data": token})
        else:
            return json.dumps({"success": False, "message": "Wrong username or password."})



def generateToken():
    letters = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ""
    for i in range(0, 35):
        token += letters[random.randint(0, 35)]
    return token


#@app.route('/signOut', methods=["POST"])
#def signOut():




@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()