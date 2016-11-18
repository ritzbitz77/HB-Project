"""SF Play Dates"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, 
    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Event, Participant)

from datetime import datetime

from random import randint


app = Flask(__name__)


app.secret_key = "ABC"

app.jinja_env.undefined = StrictUndefined

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False



@app.route('/login')
def login():

    return render_template("login.html")

@app.route('/handle-login', methods=['POST'])
def handle_login():
    '''Action for login form; log a user in.'''

    email = request.form['email']
    password = request.form['password']
    user = User.query.filter(User.email==email).first()
    

    if user:
        user_id = user.user_id
        if password == 'blah':
            session[ 'current_user' ] = user_id
            flash ('Logged in as %s' % user.email)
            return redirect ('/')

        else:
            flash ("Wrong password!")
            return redirect ('/login')

    else:
        flash ("Username not found!")
        return redirect ('/login')

 

@app.route('/')
def index():
    """User profile page"""


    user_id = session.get('current_user')
    #user_id = session[ 'current_user' ] 

    return render_template("profile.html", user_id=user_id)
  

@app.route("/create_event")
def create_event():
    """User can create an event"""



    return render_template("create_event.html")

@app.route('/create_event', methods=['POST'])
def create_event_process():

# new route here for submitted create_event/ needs to add to events table
  
    # user_id = session.get('current_user')
    # get user id out of session
    # make sure not None
    # if ok, 1) keep going 2) request User from database and then keep going
    # user = User.query.filter(User.user_id==user_id).first()
    




    event_name = request.form.get("event-name")
    date_time = request.form.get("date-time")
    location = request.form.get("location")
    notes = request.form.get("notes") 
    user_id = randint(1,7)

    event = Event(title=event_name, date_time=date_time, location=location, note=notes, user_id=user_id)

    db.session.add(event)
    db.session.commit()

    flash("Event %s added." % event_name)

    return redirect("/my_events")


@app.route("/my_events")
def my_events():
    """Users can view events they've created or rsvp'ed to"""

#not sure how to gather this info 
#session user info here

    return render_template("my_events.html")


@app.route("/events")
def events():
    """Users can see all the events occurring in San Francisco"""


    events = Event.query.order_by('date_time').all()


    return render_template("events.html", events=events)

@app.route("/event_details/<event_id>")
def event_details(event_id):
    """When browsing events, users can see details that creator has provided"""

    event = Event.query.get(event_id)
    

    return render_template("event_details.html", event=event)

@app.route("/rsvp", methods=['POST'])
def rsvp_process():

    name = request.form.get("name")
    note = request.form.get("note")

    participant = Participant(name=name, note=note) 

    users = User.query.get(user_id)
    

    #how do i get the user_id here when there is no login yet?
  

    return redirect("/my_events", users=users)
   

if __name__ == "__main__":

    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')