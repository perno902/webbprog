__author__ = 'wyz'

from flask import Flask, request, app
import database_helper
import json, random, re


app = Flask(__name__, static_url_path='')
app.debug = True

@app.route('/')
def hello():
    database_helper.init_db()
    return app.send_static_file('client.html')


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
            return json.dumps({"Success": False, "message": "No such user logged in."})

        if database_helper.signOut(token):
            return json.dumps({"Success": True, "message": "Successfully logged out."})
        else:
            return json.dumps({"Success": False, "message": "Could not log out."})


@app.route('/changePassword', methods=['POST'])
def changePassword():
    if request.method == 'POST':
        token = request.form['token']
        oldPassword = request.form['oldPassword']
        newPassword = request.form['newPassword']
        print validPassword(newPassword)
        if not validPassword(newPassword):
            return json.dumps({"success": False, "message": "Password must be 4 characters or more."})

        if database_helper.changePassword(token, oldPassword, newPassword):
            return json.dumps({"Success": True, "message": "Successfully changed password."})
        else:
            return json.dumps({"Success": False, "message": "Could not change password."})



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
            return json.dumps({"Success": True, "message": "User messages retrieved.", "data": messages})
        else:
            return json.dumps({"Success": False, "message": "Nu such user."})
    else:
        return json.dumps({"Success": False, "message": "You are not signed in."})


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
            return json.dumps({"Success": True, "message": "User data retrieved.", "data": userData})
        else:
            return json.dumps({"Success": False, "message": "Nu such user."})
    else:
        return json.dumps({"Success": False, "message": "You are not signed in."})



@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()