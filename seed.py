import datetime
from sqlalchemy import func

from model import User, Event, Participant, connect_to_db, db
from server import app




def load_users():
    """Load users from u.user into database."""

    print "User"

    for row in list(open("Users.csv"))[1:]:
        name, zipcode = row.strip().split(",")

        user = User(name=name, 
                        zipcode=zipcode)

        # We need to add to the session or it won't ever be stored
        db.session.add(user)

    db.session.commit()





# def load_event():
#     """Load users from u.user into database."""

#     print "Event"

#         event = Event(title=title, 
#                     date_time=date_time,
#                     creator=creator)


#         # We need to add to the session or it won't ever be stored
#         db.session.add(event)

#         # provide some sense of progress
#         if i % 100 == 0:
#             print i

# def load_participant():

#         print "Participant"

#         participant = Participant(user_id=user_id, 
#                     event_id=event_id)


#         # We need to add to the session or it won't ever be stored
#         db.session.add(event)

#         # provide some sense of progress
#         if i % 100 == 0:
#             print i

#     # Once we're done, we should commit our work
#     db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)

    load_users()