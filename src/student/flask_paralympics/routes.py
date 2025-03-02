# Import the Flask class from the Flask library
from flask import render_template
from flask import Blueprint

main = Blueprint('main', __name__)

# Add a route for the 'home' page
# use the route() decorator to tell Flask what URL should trigger our function.
@main.route('/')
def index():
    return render_template('index.html')

# Add a route for the user to input their name
@main.route('/name/<name>')
def name(name):
    return f"Hello {name}!"
