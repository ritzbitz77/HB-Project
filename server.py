"""SF Play Dates"""

from jinja2 import StrictUndefined

from flask import (Flask, render_template, redirect, request, flash, 
    session, jsonify)
from flask_debugtoolbar import DebugToolbarExtension

from model import (connect_to_db, db, User, Event, Participant)


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails
# silently. This is horrible. Fix this so that, instead, it raises an
# error.
app.jinja_env.undefined = StrictUndefined

app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

@app.route('/')
def index():
    """User profile page"""

    return render_template("profile.html")
  

@app.route("/create_event")
def create_event():
    """User can create an event"""



    return render_template("create_event.html")

@app.route('/create_event', methods=['POST'])
def create_event_process():

# new route here for submitted create_event/ needs to add to events table

    event_name = request.form["event-name"]
    date_time = request.form["date-time"]
    location = request.form["location"]
    notes = request.form["notes"] #need to create this in db

    event = Event(event_name=event_name, date_time=date_time, location=location, notes=notes)

    db.session.add(new_event)
    db.session.commit()

    flash("Event %s added." % event_name)

    return redirect("/my_events")


@app.route("/my_events")
def my_events():
    """Users can view events they've created or rsvp'ed to"""

#not sure how to gather this info


    return render_template("my_events.html")


@app.route("/events")
def events():
    """Users can see all the events occurring in San Francisco"""


    events = Event.query.order_by('date_time').all()

    return render_template("events.html")

@app.route("/event_details")
def event_details():
    """When browsing events, users can see details that creator has provided"""



    return render_template("event_details.html")

@app.route("/event_details", methods=['POST'])
def rsvp_process():



    return redirect("/my_events")
   

if __name__ == "__main__":

    # app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run(debug=True, host='0.0.0.0')