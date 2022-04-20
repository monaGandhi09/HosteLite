from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, FileField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError, NumberRange, Regexp
from flask_wtf.file import FileField, FileAllowed
from hostelmanagement.models import User, Application, Announcement, Complaint, MessMenu
from flask_login import current_user

class ApplicationForm(FlaskForm):
    city_choices = [('From Mumbai', 'From Mumbai'), ('Outside Mumbai', 'Outside Mumbai')]
    course_choices = [('Diploma', 'Diploma'), ('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech')]
    dept_choices = [('CS','Computer Science'), ('IT','Information Technology'), ('Electronics','Electronics')]
    college_id = IntegerField('College ID', validators=[DataRequired(), NumberRange(min=170000000, max=209999999, message="Enter a valid college-id")], render_kw={'autofocus': True})
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    city = SelectField('Resident of Mumbai', choices = city_choices, validators=[DataRequired()])
    income = IntegerField('Annual Family Income', validators=[DataRequired()])
    course = SelectField('Course', choices = course_choices, validators=[DataRequired(), Length(min=2, max=20)])
    department = SelectField('Department', choices = dept_choices, validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Contact', validators=[DataRequired(),Length(min=10, max=10), Regexp("^[0-9]*$", message="This field can only have digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Apply')

    def validate_email(self, email):
        application = Application.query.filter_by(email=email.data).first()
        user = User.query.filter_by(email=email.data).first()
        if application or user:
            raise ValidationError('An application with this email ID has already been submitted.')

    def validate_college_id(self, college_id):
        application = Application.query.filter_by(college_id=college_id.data).first()
        user = User.query.filter_by(college_id=college_id.data).first()
        if application or user:
            raise ValidationError('An application with this college ID has already been submitted.')



class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class AnnouncementForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)], render_kw={'autofocus': True})
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Announce')

class ComplaintForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=2, max=20)], render_kw={'autofocus': True})
    content = TextAreaField('Content', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Post Complaint')

class MessMenuForm(FlaskForm):
    choices = [('Breakfast', 'Breakfast'), ('Lunch', 'Lunch'), ('Dinner', 'Dinner')]
    type_of_meal = SelectField('Type of Meal', choices = choices, validators = [DataRequired()], render_kw={'autofocus': True})
    menu = TextAreaField('Menu', validators=[DataRequired(), Length(min=10)])
    image = FileField('Image File', validators=[FileAllowed(['jpg','jpeg','png'])])
    submit = SubmitField('Post Menu')

class ExitEntryForm(FlaskForm):
    student_college_id = IntegerField('Student College ID', validators=[DataRequired()], render_kw={'autofocus': True})
    entryexit = SelectField('Entry/Exit', choices = [(1, 'Entry'),(0, 'Exit')], validators = [DataRequired()])
    submit = SubmitField('Enter Record')

class VisitorsForm(FlaskForm):
    name = StringField("Visitor's Name", validators = [DataRequired(), Length(min = 3, max = 10)], render_kw={'autofocus': True})
    student_college_id = IntegerField('For Student College ID', validators=[DataRequired()])
    room_no = IntegerField('Room no.', validators=[DataRequired()])
    hostel_block = StringField('Hostel Block', validators = [DataRequired(), Length(min = 1, max = 1)])
    entryexit = SelectField('Entry/Exit', choices = [(0, 'Entry'),(1, 'Exit')], validators = [DataRequired()])
    submit = SubmitField('Enter Record')

class CouriersForm(FlaskForm):
    from_name = StringField("Sender's Name", validators = [DataRequired(), Length(min = 3, max = 10)], render_kw={'autofocus': True})
    student_college_id = IntegerField('For Student College ID', validators=[DataRequired()])
    status = SelectField('Status', choices = [(0, 'Arrived'), (1, 'Collected')], validators = [DataRequired()])
    submit = SubmitField('Enter Record')
    
class UpdateAccountForm(FlaskForm):
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    phone = StringField('Contact', validators=[DataRequired(),Length(min=10, max=10), Regexp("^[0-9]*$", message="This field can only have digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={'autofocus': True})
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email ID already in use.')

    def validate_phone(self, phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('Phone no. already in use.')

class CreateStudentForm(FlaskForm):
    city_choices = [('From Mumbai', 'From Mumbai'), ('Outside Mumbai', 'Outside Mumbai')]
    course_choices = [('Diploma', 'Diploma'), ('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech')]
    dept_choices = [('CS','Computer Science'), ('IT','Information Technology'), ('Electronics','Electronics')]
    college_id = IntegerField('College ID', validators=[DataRequired(), NumberRange(min=170000000, max=209999999, message="Enter a valid college-id")], render_kw={'autofocus': True})
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    city = SelectField('Resident of Mumbai', choices = city_choices, validators=[DataRequired()])
    income = IntegerField('Annual Family Income', validators=[DataRequired()])
    course = SelectField('Course', choices = course_choices, validators=[DataRequired(), Length(min=2, max=20)])
    department = SelectField('Department', choices = dept_choices, validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Contact', validators=[DataRequired(),Length(min=10, max=10), Regexp("^[0-9]*$", message="This field can only have digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Apply')

    def validate_email(self, email):
        application = Application.query.filter_by(email=email.data).first()
        user = User.query.filter_by(email=email.data).first()
        if application or user:
            raise ValidationError('An application with this email ID has already been submitted.')

    def validate_college_id(self, college_id):
        application = Application.query.filter_by(college_id=college_id.data).first()
        user = User.query.filter_by(college_id=college_id.data).first()
        if application or user:
            raise ValidationError('An application with this college ID has already been submitted.')

    def validate_phone(self, phone):
        application = Application.query.filter_by(phone=phone.data).first()
        user = User.query.filter_by(phone=phone.data).first()
        if application or user:
            raise ValidationError('An account with this phone already exists.')


class UpdateStudentForm(FlaskForm):

    city_choices = [('From Mumbai', 'From Mumbai'), ('Outside Mumbai', 'Outside Mumbai')]
    course_choices = [('Diploma', 'Diploma'), ('B.Tech', 'B.Tech'), ('M.Tech', 'M.Tech')]
    dept_choices = [('CS','Computer Science'), ('IT','Information Technology'), ('Electronics','Electronics')]
    college_id = IntegerField('College ID', validators=[DataRequired(), NumberRange(min=170000000, max=209999999, message="Enter a valid college-id")], render_kw={'autofocus': True})
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    course = SelectField('Course', choices = course_choices, validators=[DataRequired(), Length(min=2, max=20)])
    department = SelectField('Department', choices = dept_choices, validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')

class CreateMessStaffForm(FlaskForm):
    college_id = IntegerField('College ID', validators=[DataRequired(), NumberRange(min=170000000, max=209999999, message="Enter a valid college-id")], render_kw={'autofocus': True})
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    phone = StringField('Contact', validators=[DataRequired(),Length(min=10, max=10), Regexp("^[0-9]*$", message="This field can only have digits.")])
    email = StringField('Email', validators=[DataRequired(), Email()])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    submit = SubmitField('Submit')

    def validate_email(self, email):
        application = Application.query.filter_by(email=email.data).first()
        user = User.query.filter_by(email=email.data).first()
        if application or user:
            raise ValidationError('An account with this email ID already exists')

    def validate_college_id(self, college_id):
        application = Application.query.filter_by(college_id=college_id.data).first()
        user = User.query.filter_by(college_id=college_id.data).first()
        if application or user:
            raise ValidationError('An account with this college ID already exists.')

    def validate_phone(self, phone):
        application = Application.query.filter_by(phone=phone.data).first()
        user = User.query.filter_by(phone=phone.data).first()
        if application or user:
            raise ValidationError('An account with this phone already exists.')


class UpdateMessStaffForm(FlaskForm):

    college_id = IntegerField('College ID', validators=[DataRequired(), NumberRange(min=170000000, max=209999999, message="Enter a valid college-id")], render_kw={'autofocus': True})
    firstname = StringField('Firstname', validators=[DataRequired(), Length(min=2, max=20)])
    lastname = StringField('Lastname', validators=[DataRequired(), Length(min=2, max=20)])
    address = TextAreaField('Address', validators=[DataRequired(), Length(min=2, max=200)])
    password = PasswordField('Password', validators=[])
    confirm_password = PasswordField('Confirm Password', validators=[EqualTo('password')])
    submit = SubmitField('Update')
