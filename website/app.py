#!flask/bin/python

from flask import Flask
import flask_login 
import flask
from utils import User
import utils
from flask import Flask, jsonify, render_template
import os
import json
from flask import abort
from flask import request

app = Flask(__name__)
app.secret_key = 'SecretKey'  # Change this!

login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def index():
    #path = 'UI/Home/login_page.html'
    return  flask.redirect('login')  


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we use a class of some kind to represent and validate our
    # client-side form data. For example, WTForms is a library that will
    # handle this for us, and we use a custom LoginForm to validate.

    if flask.request.method =='POST':
        print 'Test'
        email = flask.request.form['email']
        users = utils.users
        email = str(email)
        print 'type is: ', type(email)
        try:
            print users[email]
            if users[email]:
                print 'it exists'
        except:
            print 'User does not exists'
            print email
            return 'Bad Login'


        if flask.request.form['password'] == users[email]['password']:
            user = User()
            user.id = email
            flask_login.login_user(user)
            return flask.redirect(flask.url_for('user_page'))

        return "Bad Login"


        next = flask.request.args.get('next')
    # is_safe_url should check if the url is safe for redirects.
    # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

            return flask.redirect(next or flask.url_for('index'))

    return render_template('login_page.html')   #login_page.html


@app.route('/protected')
@flask_login.login_required
def protected():
    try:
        flask_login.current_user.id
    except:
        return 'Unauthorized access'
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/user_page')
def user_page():
    """
    try:
        flask_login.current_user.id
    except:
        return 'Unauthorized access'
    """
    return render_template('user_page.html')




@app.route('/predictions/<stock_name>', methods=['GET'])
def predictions(stock_name):
    
    app_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.dirname(app_dir)
    path = os.path.join(repo_dir,'predictor')

    #stock_name = str(stock_name)
    print stock_name
    days = 5
    current_price = 350

    os.system('pythonw ' + path + '/predictor.py  %s %d %f' % (stock_name,days,current_price))
    prediction_file = os.path.join(path,'predictions.json')

    ## read the above prediction 
    f = open(prediction_file,'r')
    prediction_data = json.load(f)
    f.close()
    prediction_data['success'] = True


    return flask.jsonify(prediction_data, )




@login_manager.user_loader
def user_loader(email):
    if email not in utils.users:
        return

    user = User()
    user.id = email
    return user

@login_manager.request_loader
def request_loader(request):
    try:
        email = request.form.get('email')

    except:
        return 'Unauthorized access'
    if email not in utils.users:
        return

    user = User()
    user.id = email

    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!
    user.is_authenticated = request.form['password'] == users[email]['password']

    return user


@app.route('/logout')
def logout():
    flask_login.logout_user()
    return 'Logged out'

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized'



## this is the starting page which makes a random prediction for AAPL stock for 2 days 
## just to make sure that the services is up and running!
@app.route('/neural_predictor', methods=['GET'])
#@flask_login.login_required
def neural_predictor():
    app_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.dirname(app_dir)
    path = os.path.join(repo_dir,'predictor')

    #path = '/Users/giorgoschantzialexiou/Repositories/stock_prediction_web_app/predictor'
    stock_name = 'AAPL'
    days = 2
    current_price = 350

    os.system('python ' + path + '/predictor.py  %s %d %f' % (stock_name,days,current_price))
    prediction_file = os.path.join(path,'predictions.json')

    ## read the above prediction 
    f = open(prediction_file,'r')
    prediction_data = json.load(f)
    f.close()
    prediction_data['success'] = True


    return flask.jsonify(prediction_data)

## creating actual stock predictor

@app.route('/neural_predictor/<stock_name>/<days>/<current_price>', methods=['GET'])
def test(stock_name,days,current_price):

    #path = '/Users/giorgoschantzialexiou/Repositories/stock_prediction_web_app/predictor'
    app_dir = os.path.dirname(os.path.realpath(__file__))
    repo_dir = os.path.dirname(app_dir)
    path = os.path.join(repo_dir,'predictor')

    days = int(days)
    current_price = float(current_price)

    try:
        os.system('python ' + path + '/predictor.py  %s %d %f' % (stock_name,days,current_price))
        prediction_file = os.path.join(path,'predictions.json')

        ## read the above prediction 
        f = open(prediction_file,'r')
        prediction_data = json.load(f)
        f.close()

        prediction_data['success'] = True
    except:
        abort(404)


    return flask.jsonify(prediction_data)

if __name__ == '__main__':

#    global login_manager
#    login_manager = flask_login.LoginManager()
#    login_manager.init_app(app)

    app.run(debug=True)
