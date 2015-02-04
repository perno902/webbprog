__author__ = 'wyz'

from flask import Flask, request, app
import database_helper
import json


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    database_helper.init_db()
    #signUp()
    #database_helper.testdb()

    return "world, hello"

"""
def userExist(email):
    return database_helper.checkUser(email)
"""

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

        if (len(email) == 0) or (len(password) == 0) or (len(firstname) == 0) or (len(familyname) == 0) or (len(gender) == 0) or (len(city) == 0) or (len(country) == 0):
            return json.dumps({"success": False, "message": "Incomplete forms"})

        result = database_helper.signUpUser(email, password, firstname, familyname, gender, city, country)


        if result:
            return json.dumps({"success": True, "message": "Successfully created user!"})
        else:
            return json.dumps({"success": False, "message": "User already exists"})



    """else:
        return json.dumps({"success": False, "message": "User already exists"})
"""

#email, password, firstname, familyname, gender, city, country

@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()