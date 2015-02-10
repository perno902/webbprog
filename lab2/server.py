__author__ = 'wyz'

from flask import Flask, request, app
import database_helper
import json, random


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    database_helper.init_db()

    return "world, hello"



#<email>/<password>/<firstname>/<familyname>/<gender>/<city>/<country>'
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

        result = database_helper.signUpUser(email, password, firstname, familyname, gender, city, country)
        if result:
            return json.dumps({"success": True, "message": "Successfully created user!"})
        else:
            return json.dumps({"success": False, "message": "User already exists"})


def generateToken():
    letters = "abcdefghiklmnopqrstuvwwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890"
    token = ''.join(random.choice(letters) for _ in range(len(str(letters))))
    return token

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
        userEmail = database_helper.getToken(token)
        messages = database_helper.getMessages(userEmail)
        return json.dumps({"Success": True, "message": "User messages retrieved.", "data": messages})

@app.route('/getMessagesByEmail', methods=["GET"])
def getMessagesByEmail():
    if request.method == 'GET':
        # kolla om request.args.get('token') finns
        userEmail = request.args.get('email')
        messages = database_helper.getMessages(userEmail)
        return json.dumps({"Success": True, "message": "User messages retrieved.", "data": messages})


@app.route('/signOut', methods=['POST'])
def signOut():
    if request.method == 'POST':
        email = request.form['email']
        # token = database_helper.getToken(email)
        if database_helper.signOut(email):
            return json.dumps({"Success": True, "message": "Successfully logged out."})
        else:
            return json.dumps({"Success": False, "message": "Could not log out."})





@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()