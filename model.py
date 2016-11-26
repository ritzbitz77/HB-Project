from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    """User information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String, nullable=False, unique=True)
    name = db.Column(db.String(65), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)
   

    events =  db.relationship("Event", 
                                secondary="participants",
                                backref ="attendees")
    
    

    rsvp = db.relationship("Participant",
                            backref = "user")
    #relationship between the users and participants table


    def __repr__(self):

        return "<User user_id=%s name=%s>" % (self.user_id, self.name)



class Event(db.Model):
    """User created events"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=True)
    date_time = db.Column(db.DateTime, nullable=True)
    location = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True) #this is where we are getting host from
    note = db.Column(db.UnicodeText, nullable=False)

    host = db.relationship("User",
                            backref="host_events")
    #relationship between host and event. User_id is coming from the Event table.

    participants = db.relationship("Participant", backref="event")
    #relationship between participants and the event



    def __repr__(self):


        s = "<event_id=%s title=%s date_time=%s user_id=%s, note=%s>"
        return s % (self.event_id, self.title, self.date_time, self.user_id, self.note)



class Participant(db.Model):
    """List of participants attending an event"""

    __tablename__ = "participants"

    rsvp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), 
                        nullable=False)
    note = db.Column(db.UnicodeText, nullable=False)
    
    
    def __repr__(self):

        s = "<Event event_id=%s user_id=%s>"
        return s % (self.event_id, self.user_id)


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sfplaydates'
    db.app = app
    db.init_app(app)

def example_data():
    """Create example data for the test database."""
    
    Event.query.delete()
    
    rp = Event(title="Playdate at Rossi Park", 
               date_time='2016-11-18 14:00:00', 
               location="Angelo J. Rossi Playground, Willard North, San Francisco, CA, United States ", 
               user_id=1, 
               note="Snacks!")
    ggp = Event(title="Playdate at GGP", 
                date_time='2016-11-28 16:00:00', 
                location="Mother's Meadow Playground, Martin Luther King Junior Drive, San Francisco, CA, United States", 
                user_id=2, 
                note="Snacks!")
    pp = Event(title="Playdate at the Panhandle Park", 
               date_time='2016-12-08 10:00:00', 
               location="The Panhandle, San Francisco, CA, United States", 
               user_id=3, 
               note="Snacks!")
    al = Event(title="Playdate at Alamo Square", 
               date_time='2016-12-05 10:00:00', 
               location="Alamo Square, San Francisco, CA, United States",  
               user_id=4, 
               note="Snacks!")
    kp = Event(title="Playdate at Koret Park", 
               date_time='2016-12-02 09:00:00', 
               location="Koret Park, San Francisco, CA, United States", 
               user_id=5, 
               note="Snacks!")
    aa = Participant(user_id=10,
                     event_id=2,
                     note="I'll also bring snacks!")
    ab = Participant(user_id=11,
                     event_id=2,
                     note="I'll also bring snacks!")
    ac = Participant(user_id=12,
                     event_id=3,
                     note="I'll also bring snacks!")
    ad = Participant(user_id=13,
                     event_id=3 ,
                     note="I'll also bring snacks!")
    ae = Participant(user_id=14,
                     event_id=4,
                     note= "I'll also bring snacks!")

    db.session.add_all([rp, ggp, pp, al, kp, aa, ab, ac, ad, ae])

    db.session.commit()
    




if __name__ == "__main__":

    from server import app
    connect_to_db(app)
    print "Connected to DB."