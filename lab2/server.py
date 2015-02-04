__author__ = 'wyz'

from flask import Flask, request, app
import database_helper


app = Flask(__name__)
app.debug = True

@app.route('/')
def hello():
    database_helper.init_db()
    database_helper.testdb()
    #signUp("test", "herp", "hej", "da", "male", "link", "swe")
    return "hello world!"


@app.route('/signUp/<email>/<password>/<firstname>/<familyname>/<gender>/<city>/<country>', methods=["POST"])
def signUp(email, password, firstname, familyname, gender, city, country):
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        firstname = request.form['firstname']
        familyname = request.form['familyname']
        gender = request.form['gender']
        city = request.form['city']
        country = request.form['country']
        result = database_helper.signUpUser(email, password, firstname, familyname, gender, city, country)

        if(result):
            return "Contact added"
        else:
            "Could not add contact"



@app.teardown_appcontext
def teardown_app(exception):
    database_helper.close()


if __name__ == '__main__':
    app.run()