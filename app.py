from flask import Flask, send_file, request
from main import create_image
from email_helper import *
from user_management import *
app = Flask(__name__)


@app.route('/')
def home():
    return send_file("static/home.txt")


@app.route('/get_image') #requires interests
def get_image_route():
    interests = request.args.get('interests')
    
    image = create_image(interests) #from main.py
    return send_file(image)

@app.route('/mail_users') #requires frequency
def mail_users_route():
    frequency = request.args.get('frequency').title()

    if frequency not in ['Daily', 'Weekly', 'Fortnight', 'Monthly']:
        return "Invalid frequency. Valid values are 'Daily', 'Weekly', 'Fortnight', and 'Monthly'"
        
    return mail_users(frequency) #from user_management.py, returns success msg


@app.route('/unsubscribe') #requires id
def unsubscribe_route():
    id = request.args.get('id')
    
    return delete_user(id) #from user_management.py, returns success msg

@app.route('/add_user')
def add_user_route():
    # Eg: /add_user?name=Prakhar%20Aditya%20Tripathi&email=prakhar.ad.tr@gmail.com&interests=motivation,inspiration&frequency=Daily
    name = request.args.get('name').replace("%20", " ")
    email = request.args.get('email')
    interests = request.args.get('interests')
    frequency = request.args.get('frequency').title()
    
    return addUser(name, email, interests, frequency) #from user_management.py, returns success msg





if __name__ == '__main__':
    app.run(debug=True)