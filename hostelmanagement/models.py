from datetime import datetime
from hostelmanagement import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.String(9), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    course = db.Column(db.String(20),nullable=True)
    department = db.Column(db.String(20), nullable=True)
    user_type = db.Column(db.Integer, nullable = False, default=1)
    room_no = db.Column(db.Integer, nullable = True)
    #admin-0, student-1, guard-2, messstaff-3, CR-4
    announcements = db.relationship('Announcement', backref='author', lazy=True)
    complaints = db.relationship('Complaint', backref='author', lazy=True)
    mess_menu = db.relationship('MessMenu', backref='author', lazy=True)
    courier = db.relationship('Courier', backref='user', lazy=True)
    exitentry = db.relationship('ExitEntry', backref='user', lazy=True)
    visitor = db.relationship('Visitor', backref='user', lazy=True)

    def __repr__(self):
        return f"User('{self.college_id}', '{self.firstname}', '{self.lastname}')"

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    college_id = db.Column(db.String(9), unique=True, nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(10), unique=True, nullable=False)
    address = db.Column(db.Text, nullable=False)
    city = db.Column(db.String(10), nullable=False)
    income = db.Column(db.Integer, nullable=False)
    course = db.Column(db.String(20),nullable=False)
    department = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    status = db.Column(db.Integer, nullable=False, default=0)
    #0-->pending 1-->alloted

    def __repr__(self):
        return f"Application('{self.college_id}', '{self.firstname}', '{self.lastname}')"

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Announcement('{self.title}', '{self.date_posted}')"

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Unresolved")
    answers = db.relationship('Answer', backref = 'complaint', lazy = True)

    def __repr__(self):
        return f"Complaint('{self.title}', '{self.date_posted}')"

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    complaint_id = db.Column(db.Integer, db.ForeignKey('complaint.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Answer('{self.id}', '{self.complaint_id}')"

class MessMenu(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    type_of_meal = db.Column(db.String(100), nullable = False)
    menu = db.Column(db.Text, nullable = False)
    image = db.Column(db.String(20), nullable = False, default = 'food.jpg')
    date_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"MessMenu('{self.type_of_meal}', '{self.date_posted}')"

class Room(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    hostel_block = db.Column(db.String(1), nullable = False)
    room_no = db.Column(db.Integer, nullable = False)
    capacity = db.Column(db.Integer, nullable = False, default = 3)
    student1_id = db.Column(db.Integer, nullable = True)
    student2_id = db.Column(db.Integer, nullable = True)
    student3_id = db.Column(db.Integer, nullable = True)

    def __repr__(self):
        return f"Room('{self.room_no}', '{self.hostel_block}')"

class Courier(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    from_name = db.Column(db.String(10), nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 0)
    # 0->arrived, 1->collected
    date_arrived = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Courier('{self.room_no}', '{self.hostel}')"

class ExitEntry(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 0)
    # 0 -> exit, 1-> entry
    datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"ExitEntry('{self.user_id}','{self.status}', '{self.datetime}')"

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(10), nullable = False)
    hostel_block = db.Column(db.String(1), nullable = False)
    room_no = db.Column(db.Integer, nullable = False)
    for_user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    status = db.Column(db.Integer, nullable = False, default = 0)
    # 0 -> entered, 1-> exited
    datetime = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)

    def __repr__(self):
        return f"Visitor('{self.name}', '{self.for_user_id}','{self.status}', '{self.datetime}')"
