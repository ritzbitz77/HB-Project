from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class User(db.Model):
    """User information"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String(65), nullable=False)
    zipcode = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s name=%s>" % (self.user_id, self.name)



class Event(db.Model):
    """User created events"""

    __tablename__ = "events"

    event_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String, nullable=True)
    date_time = db.Column(db.DateTime, nullable=True)
    creator = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<event_id=%s title=%s date_time=%s creator=%s>"
        return s % (self.event_id, self.title, self.date_time, self.creator)



class Participant(db.Model):
    """List of participants attending an event"""

    __tablename__ = "participants"

    rsvp_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), 
                        nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("events.event_id"), 
                        nullable=False)
    
    #Define relationship to user
    user = db.relationship("User", 
                            backref=db.backref("events", 
                                            order_by=event_id))
    
    def __repr__(self):
        """Provide helpful representation when printed."""

        s = "<Event event_id=%s user_id=%s>"
        return s % (self.event_id, self.user_id)

##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///sfplaydates'
    db.app = app
    db.init_app(app)

# def example_data():
#     """Create example data for the test database."""
    
#     Participant.query.delete()
    
    # tr = Game(name = "Ticket to Ride", description = "a cross-country train adventures")
    # pg = Game(name = "Power Grid", description = "supply the most cities with power" )
    # al = Game(name="Amazing Labyrinth", description="move around the shifting paths of the labyrinth in a race to collect various treasures")
    # pf = Game(name="Princes of Florence", description="attract artists and scholars trying to become the most prestigious family in Florence")
    # ag = Game(name="Agricola", description="farmers sow, plow the fields, collect wood, and feed their families"
    




if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."