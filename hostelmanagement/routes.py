from flask import render_template, url_for, flash, redirect, request
from hostelmanagement import app, db, bcrypt
from hostelmanagement.forms import ApplicationForm, LoginForm, ComplaintForm, AnnouncementForm, MessMenuForm, UpdateAccountForm, CreateStudentForm, UpdateStudentForm, CreateMessStaffForm, UpdateMessStaffForm, ExitEntryForm, VisitorsForm,CouriersForm
from hostelmanagement.models import User, Application, Announcement, Complaint, Answer, MessMenu, Courier, ExitEntry, Visitor, Room
from flask_login import login_user, current_user, logout_user, login_required
from hostelmanagement import mail
from flask_mail import Mail, Message
import datetime
import os
import secrets
import string, random
from PIL import Image

@app.route("/")
def index():
    return render_template('index.html')

@app.route("/home")
def home():
    announcements = Announcement.query.all()
    return render_template('home.html', announcements = announcements)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/contact")
def contact():
    return render_template('contact.html')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard_mapping'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('dashboard_mapping'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('account/login.html', title='Login', form=form)

@app.route('/dashboard')
@login_required
def dashboard_mapping():
    if current_user.user_type == 0:     # admin
        return redirect(url_for('announcement_list'))
        
    elif current_user.user_type == 1:   # student
        return redirect(url_for('display_student_announcements'))

    elif current_user.user_type == 2:   # guard
        return redirect(url_for('display_guard_announcements'))

    elif current_user.user_type == 3:   # mess
        return redirect(url_for('display_mess_announcements'))
    
    elif current_user.user_type == 4:   # cr
        return redirect(url_for('display_announcements'))

    return "User does not exist"

    
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/application", methods=['GET', 'POST'])
def application():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = ApplicationForm()
    if form.validate_on_submit():
        application = Application(firstname = form.firstname.data, lastname = form.lastname.data,
                            college_id = form.college_id.data, phone = form.phone.data,
                            department = form.department.data, course = form.course.data,
                            address = form.address.data, city = form.city.data, 
                            income = form.income.data, email=form.email.data)
        db.session.add(application)
        db.session.commit()

        msg = Message("Send Mail Tutorial!",
                sender="monagandhi09@gmail.com",
                recipients=["harshildoshi6333@gmail.com"])
        msg.body = "Yo!\nHave you heard the good word of Python???"           
        mail.send(msg)
        print("Mail sent")
        flash('You have applied to the Hostel. Please keep checking your email inbox for further updates.', 'success')
        return redirect(url_for('index'))
    return render_template('account/apply.html', title='Application', form=form)



###############STUDENT ROUTES#####################
@app.route("/student/announcements")
@login_required
def display_student_announcements():
    user = current_user
    announcements = Announcement.query.all()
    return render_template('student/announcements.html', title = 'Announcements', announcements = announcements, user=user)

@app.route("/students/mess")
@login_required
def mess_menu():
    messMenu = MessMenu.query.filter_by()
    return render_template('student/mess_menu.html', title = 'Mess Menu', messMenu = messMenu)

@app.route("/students/complaints")
@login_required
def display_complaints():
    complaints = Complaint.query.all()
    return render_template('student/complaints.html', title = 'Complaints', complaints = complaints)

@app.route("/students/complaints/new", methods=['GET', 'POST'])
@login_required
def new_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been successfully registered!', 'success')
        return redirect(url_for('display_complaints'))
    return render_template('student/create_complaint.html', title='New Complaint', form = form)

@app.route("/students/couriers")
@login_required
def display_couriers():
    pending_couriers = Courier.query.filter_by(user_id = current_user.id, status=0)
    collected_couriers = Courier.query.filter_by(user_id = current_user.id, status=1)
    return render_template('student/couriers.html', title = 'Couriers', pending_couriers = pending_couriers, collected_couriers = collected_couriers)

@app.route("/students/entry_exits")
@login_required
def display_entry_exits():
    entries = ExitEntry.query.filter_by(user_id = current_user.id)
    visitors = Visitor.query.filter_by(for_user_id = current_user.id)
    return render_template('student/entry_exit.html', title = 'Entry-Exits', entries = entries, visitors = visitors)

@app.route("/students/update", methods=['GET', 'POST'])
@login_required
def update_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        
        if form.password.data and form.confirm_password.data:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed! Login with new password.', 'success')
            return redirect(url_for('logout'))
        else:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('update_account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('student/update.html', title='Account', form=form)




###########MESS STAFF ROUTES############################
@app.route("/mess_staff/announcements")
@login_required
def display_mess_announcements():
    user = current_user
    announcements = Announcement.query.all()
    return render_template('mess_staff/announcements.html', title = 'Announcements', announcements = announcements, user=user)

@app.route("/mess_staff/mess")
@login_required
def display_menu():
    messMenu = MessMenu.query.all()
    return render_template('mess_staff/mess_menu.html', title = 'Mess Menu', messMenu = messMenu)

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/menu_pics', picture_fn)

    output_size = (300, 300)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

@app.route("/mess_staff/update_menu/<int:id>", methods=['GET', 'POST'])
@login_required
def update_menu(id):
    messMenu = MessMenu.query.get_or_404(id)
    #iske liye sirf dhyaan rakhna hai ki menu ka author staff hi ho
    if messMenu.author != current_user:
        abort(403)
    form = MessMenuForm()
    if form.validate_on_submit():
        messMenu.type_of_meal = form.type_of_meal.data
        messMenu.menu = form.menu.data
        messMenu.date_posted = datetime.datetime.now()
        if form.image.data:
            picture_file = save_picture(form.image.data)
            messMenu.image = picture_file
        db.session.commit()
        flash('Your menu has been updated!', 'success')
        return redirect(url_for('display_menu'))
    elif request.method == 'GET':
        form.type_of_meal.data = messMenu.type_of_meal
        form.menu.data = messMenu.menu
        form.image.data = messMenu.image
    return render_template('mess_staff/update_menu.html', title='Update Menu', form = form)

@app.route("/mess_staff/update", methods=['GET', 'POST'])
@login_required
def update_mess_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.password.data and form.confirm_password.data:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed! Login with new password.', 'success')
            return redirect(url_for('logout'))
        else:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('update_mess_account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('mess_staff/update.html', title='Account', form=form)


###############CR ROUTES########################

@app.route("/cr/announcements")
@login_required
def display_announcements():
    user = current_user
    announcements = Announcement.query.all()
    return render_template('cr/announcements.html', title = 'Announcements', announcements = announcements, user=user)

@app.route("/cr/announcements/<int:announcement_id>")
def announcement(announcement_id):
    user = current_user
    single_announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('cr/announcement.html', title=single_announcement.title, single_announcement=single_announcement, user=user)

@app.route("/cr/announcements/new", methods=['GET', 'POST'])
@login_required
def new_announcement():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(announcement)
        db.session.commit()
        flash('Your announcement has been successfully published!', 'success')
        return redirect(url_for('display_announcements'))
    return render_template('cr/create_announcement.html', title='New Announcement', form = form)

@app.route("/cr/announcements/<int:announcement_id>/update", methods=['GET', 'POST'])
@login_required
def update_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    if announcement.author != current_user:
        abort(403)
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash('Your announcement has been updated!', 'success')
        return redirect(url_for('display_announcements'))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    return render_template('cr/create_announcement.html', title='Update Post', form=form)


@app.route("/cr/announcements/<int:announcement_id>/delete", methods=['POST'])
@login_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    if announcement.author != current_user:
        abort(403)
    db.session.delete(announcement)
    db.session.commit()
    flash('Your announcement has been deleted!', 'success')
    return redirect(url_for('display_announcements'))

@app.route("/cr/mess")
@login_required
def cr_mess_menu():
    messMenu = MessMenu.query.all()
    return render_template('cr/mess_menu.html', title = 'Mess Menu', messMenu = messMenu)

@app.route("/cr/complaints")
@login_required
def display_cr_complaints():
    complaints = Complaint.query.filter_by(user_id = current_user.id)
    return render_template('cr/complaints.html', title = 'Complaints', complaints = complaints)

@app.route("/cr/complaints/new", methods=['GET', 'POST'])
@login_required
def new_cr_complaint():
    form = ComplaintForm()
    if form.validate_on_submit():
        complaint = Complaint(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(complaint)
        db.session.commit()
        flash('Your complaint has been successfully registered!', 'success')
        return redirect(url_for('display_cr_complaints'))
    return render_template('cr/create_complaint.html', title='New Complaint', form = form)

@app.route("/cr/couriers")
@login_required
def display_cr_couriers():
    pending_couriers = Courier.query.filter_by(user_id = current_user.id, status=0)
    collected_couriers = Courier.query.filter_by(user_id = current_user.id, status=1)
    return render_template('cr/couriers.html', title = 'Couriers', pending_couriers = pending_couriers, collected_couriers = collected_couriers)

@app.route("/cr/entry_exits")
@login_required
def display_cr_entry_exits():
    entries = ExitEntry.query.filter_by(user_id = current_user.id)
    visitors = Visitor.query.filter_by(for_user_id = current_user.id)
    return render_template('cr/entry_exit.html', title = 'Entry-Exits', entries = entries, visitors = visitors)

@app.route("/cr/update", methods=['GET', 'POST'])
@login_required
def update_cr_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.password.data and form.confirm_password.data:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed! Login with new password.', 'success')
            return redirect(url_for('logout'))
        else:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('update_cr_account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('cr/update.html', title='Account', form=form)


##############GUARD ROUTES######################
@app.route("/guard/announcements")
@login_required
def display_guard_announcements():
    user = current_user
    announcements = Announcement.query.all()
    return render_template('guard/announcements.html', title = 'Announcements', announcements = announcements, user=user)

@app.route('/guard/entryexit')
@login_required
def entry_exit_records():
    entryexits = ExitEntry.query.all()
    return render_template('guard/entryexit.html', entryexits = entryexits)

@app.route('/guard/entryexit/new', methods = ['GET', 'POST'])
@login_required
def new_entry_exit_record():
    form = ExitEntryForm()
    if form.validate_on_submit():
        status = form.entryexit.data
        user = User.query.filter_by(college_id = form.student_college_id.data).first()
        exit_entry = ExitEntry(status=status, user = user)
        db.session.add(exit_entry)
        db.session.commit()
        flash('Entry created!', 'success')
        return redirect(url_for('entry_exit_records'))
    return render_template('guard/create_entryexit.html', title='New Record',form=form)


@app.route('/guard/visitors')
@login_required
def visitors_records():
    visitors = Visitor.query.all()
    return render_template('guard/visitors.html', visitors = visitors)

@app.route('/guard/visitors/new', methods = ['GET', 'POST'])
@login_required
def new_visitor_record():
    form = VisitorsForm()
    if form.validate_on_submit():
        status = form.entryexit.data
        user = User.query.filter_by(college_id = form.student_college_id.data).first()
        visitor = Visitor(name = form.name.data, hostel_block = form.hostel_block.data, room_no = form.room_no.data,
        status = status, user = user)
        db.session.add(visitor)
        db.session.commit()
        flash('Entry created!', 'success')
        return redirect(url_for('visitors_records'))
    return render_template('guard/create_visitor.html', title='New Record',                    
    form=form)

@app.route('/guard/couriers')
@login_required
def couriers_records():
    couriers = Courier.query.all()
    return render_template('guard/couriers.html', couriers = couriers)

@app.route('/guard/couriers/new', methods = ['GET', 'POST'])
@login_required
def new_courier_record():
    form = CouriersForm()
    if form.validate_on_submit():
        user = User.query.filter_by(college_id = form.student_college_id.data).first()
        courier = Courier(user = user, from_name = form.from_name.data, status = form.status.data)
        db.session.add(courier)
        db.session.commit()
        flash('Entry created', 'success')
        return redirect(url_for('couriers_records'))
    return render_template('guard/create_courier.html', form=form)

@app.route("/guard/update", methods=['GET', 'POST'])
@login_required
def update_guard_account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.password.data and form.confirm_password.data:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Password changed! Login with new password.', 'success')
            return redirect(url_for('logout'))
        else:
            current_user.email = form.email.data
            current_user.phone = form.phone.data
            current_user.address = form.address.data
            db.session.commit()
            flash('Your account has been updated!', 'success')
            return redirect(url_for('update_guard_account'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.address.data = current_user.address
        form.phone.data = current_user.phone
    return render_template('guard/update.html', title='Account', form=form)

##############ADMIN ROUTES######################

@app.route('/admin/applications')
@login_required
def display_applications():
    pending_apps = Application.query.filter_by(status=0)
    confirmed_apps = Application.query.filter_by(status=1)
    return render_template('admin/applications.html',title='Application', pending_apps=pending_apps, confirmed_apps = confirmed_apps)

@app.route('/admin/applications/<int:id>' ,methods=['GET','POST'])
@login_required
def individual_applications(id):

    if request.method=='POST':
        room = Room.query.filter(Room.capacity>0).order_by(Room.capacity).first()
        if room:
            application = Application.query.get_or_404(id)
            password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
            user = User(college_id=application.college_id,firstname=application.firstname,lastname=application.lastname,
            email=application.email,password=hashed_password,phone=application.phone,address=application.address,course=application.course,department=application.department)

            room.capacity-=1
            application.status=1
            user.room_no = room.room_no
            db.session.add(user)
            db.session.commit()

            user = User.query.filter_by(college_id=application.college_id).first()
            if not room.student1_id:
                room.student1_id = user.id
            
            elif not room.student2_id:
                room.student2_id = user.id

            else:
                room.student3_id = user.id

            db.session.commit()


            msg = Message("Password for HosteLite",
                sender="monagandhi09@gmail.com",
                recipients=["harshildoshi6333@gmail.com"])
            msg.body = "The password for your hostelite account is: "  + password + "\nPlease reset your password as soon as you login."      
            mail.send(msg)
        return redirect(url_for('display_applications'))

    application = Application.query.get_or_404(id)
    return render_template('admin/individual_application.html', application=application)

@app.route('/admin/student' ,methods=['GET','POST'])
@login_required
def student_list():

    users = User.query.filter_by(user_type=1)

    return render_template('admin/student_list.html', users = users)

@app.route('/admin/student/create' ,methods=['GET','POST'])
@login_required
def student_create():

    form = CreateStudentForm()
    if form.validate_on_submit():
        application = Application(firstname = form.firstname.data, lastname = form.lastname.data,
                            college_id = form.college_id.data, phone = form.phone.data,
                            department = form.department.data, course = form.course.data,
                            address = form.address.data, city = form.city.data, 
                            income = form.income.data, email=form.email.data)
        db.session.add(application)
        db.session.commit()
        flash('Application submitted successfully.', 'success')
        return redirect(url_for('student_list'))

    return render_template('admin/student_create.html', form=form)

@app.route('/admin/student/update/<int:id>' ,methods=['GET','POST'])
@login_required
def student_update(id):
    user=User.query.get_or_404(id)
    form=UpdateStudentForm()

    if form.validate_on_submit():
        user.college_id = form.college_id.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.address = form.address.data
        user.course = form.course.data
        user.department = form.department.data

        if form.password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password

        db.session.commit()
        flash('Account information has been updated!', 'success')
        return redirect(url_for('student_list'))

    elif request.method == 'GET':
        form.college_id.data = user.college_id
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.address.data = user.address
        form.course.data = user.course
        form.department.data = user.department

    return render_template('admin/update_student_info.html', title='Update', form=form, user=user)

@app.route('/admin/student/delete/<int:id>' ,methods=['POST'])
@login_required
def student_delete(id):
    user = User.query.get_or_404(id)
    announcements = Announcement.query.filter_by(user_id = id).delete()
    complaints = Complaint.query.filter_by(user_id = id).delete()
    answers = Answer.query.filter_by(user_id = id).delete()
    couriers = Courier.query.filter_by(user_id = id).delete()
    exitentries = ExitEntry.query.filter_by(user_id = id).delete()
    visitors = Visitor.query.filter_by(for_user_id = id).delete()
    room = Room.query.filter_by(room_no = user.room_no).first()

    print("Before Removing student from room:")
    print(room.student1_id)
    print(room.student2_id)
    print(room.student3_id)
    
    if room.student1_id == id:
        room.student1_id = None
    elif room.student2_id == id:
        room.student2_id = None
    elif room.student3_id == id:
        room.student3_id = None

    print("After Removing student from room:")    
    print(room.student1_id)
    print(room.student2_id)
    print(room.student3_id)

    db.session.delete(user)
    room.capacity += 1
    db.session.commit()
    
    room = Room.query.filter_by(room_no = user.room_no).first()
    print("After changing capacity:")
    print(room.student1_id)
    print(room.student2_id)
    print(room.student3_id)
    print(room.capacity)
    flash('User successfully Deleted!', 'success')
    return redirect(url_for('student_list'))
    

@app.route('/admin/messstaff' ,methods=['GET','POST'])
@login_required
def messstaff_list():

    users = User.query.filter_by(user_type=3)
    return render_template('admin/messstaff_list.html', users = users)

@app.route('/admin/messstaff/create' ,methods=['GET','POST'])
@login_required
def messstaff_create():

    form = CreateMessStaffForm()
    if form.validate_on_submit():
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(firstname = form.firstname.data, lastname = form.lastname.data,
                            college_id = form.college_id.data, phone = form.phone.data,
                            address = form.address.data, email=form.email.data,password=hashed_password,user_type=3)
        db.session.add(user)
        db.session.commit()
        msg = Message("Password for HosteLite",
                sender="monagandhi09@gmail.com",
                recipients=["harshildoshi6333@gmail.com"])
        msg.body = "The password for your hostelite account is: "  + password + "\nPlease reset your password as soon as you login."      
        mail.send(msg)
        flash('Account created successfully.', 'success')
        return redirect(url_for('messstaff_list'))
        
    return render_template('admin/messstaff_create.html', form=form)

@app.route('/admin/messstaff/update/<int:id>' ,methods=['GET','POST'])
@login_required
def messstaff_update(id):
    user=User.query.get_or_404(id)
    form=UpdateMessStaffForm()

    if form.validate_on_submit():
        user.college_id = form.college_id.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.address = form.address.data

        if form.password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password

        db.session.commit()
        flash('Account information has been updated!', 'success')
        return redirect(url_for('messstaff_list'))

    elif request.method == 'GET':
        form.college_id.data = user.college_id
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.address.data = user.address

    return render_template('admin/update_messstaff_info.html', title='Update', form=form, user=user)

@app.route('/admin/messstaff/delete/<int:id>' ,methods=['POST'])
@login_required
def messstaff_delete(id):
    user = User.query.get_or_404(id)
    announcements = Announcement.query.filter_by(user_id = id).delete()
    complaints = Complaint.query.filter_by(user_id = id).delete()
    answers = Answer.query.filter_by(user_id = id).delete()
    couriers = Courier.query.filter_by(user_id = id).delete()
    exitentries = ExitEntry.query.filter_by(user_id = id).delete()
    visitors = Visitor.query.filter_by(for_user_id = id).delete()

    db.session.delete(user)
    db.session.commit()
    flash('User successfully Deleted!', 'success')
    return redirect(url_for('messstaff_list'))

@app.route('/admin/cr' ,methods=['GET','POST'])
@login_required
def cr_list():

    users = User.query.filter_by(user_type=4)
    return render_template('admin/cr_list.html', users = users)

@app.route('/admin/cr/create' ,methods=['GET','POST'])
@login_required
def cr_create():

    form = CreateMessStaffForm()
    if form.validate_on_submit():
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(firstname = form.firstname.data, lastname = form.lastname.data,
                            college_id = form.college_id.data, phone = form.phone.data,
                            address = form.address.data, email=form.email.data,password=hashed_password,user_type=4)
        db.session.add(user)
        db.session.commit()
        msg = Message("Password for HosteLite",
                sender="monagandhi09@gmail.com",
                recipients=["harshildoshi6333@gmail.com"])
        msg.body = "The password for your hostelite account is: "  + password + "\nPlease reset your password as soon as you login."      
        mail.send(msg)
        flash('Account created successfully.', 'success')        
        return redirect(url_for('cr_list'))
        
    return render_template('admin/cr_create.html', form=form)

@app.route('/admin/cr/update/<int:id>' ,methods=['GET','POST'])
@login_required
def cr_update(id):
    user=User.query.get_or_404(id)
    form=UpdateMessStaffForm()

    if form.validate_on_submit():
        user.college_id = form.college_id.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.address = form.address.data

        if form.password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password

        db.session.commit()
        flash('Account information has been updated!', 'success')
        return redirect(url_for('cr_list'))

    elif request.method == 'GET':
        form.college_id.data = user.college_id
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.address.data = user.address

    return render_template('admin/update_cr_info.html', title='Update', form=form, user=user)

@app.route('/admin/cr/delete/<int:id>' ,methods=['POST'])
@login_required
def cr_delete(id):
    user = User.query.get_or_404(id)
    announcements = Announcement.query.filter_by(user_id = id).delete()
    complaints = Complaint.query.filter_by(user_id = id).delete()
    answers = Answer.query.filter_by(user_id = id).delete()
    couriers = Courier.query.filter_by(user_id = id).delete()
    exitentries = ExitEntry.query.filter_by(user_id = id).delete()
    visitors = Visitor.query.filter_by(for_user_id = id).delete()

    db.session.delete(user)
    db.session.commit()
    flash('User successfully Deleted!', 'success')
    return redirect(url_for('cr_list'))

@app.route('/admin/guard' ,methods=['GET','POST'])
@login_required
def guard_list():

    users = User.query.filter_by(user_type=2)
    return render_template('admin/guard_list.html', users = users)

@app.route('/admin/guard/create' ,methods=['GET','POST'])
@login_required
def guard_create():

    form = CreateMessStaffForm()
    if form.validate_on_submit():
        password = ''.join(random.choices(string.ascii_uppercase + string.digits, k = 8))
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(firstname = form.firstname.data, lastname = form.lastname.data,
                            college_id = form.college_id.data, phone = form.phone.data,
                            address = form.address.data, email=form.email.data,password=password,user_type=2)
        db.session.add(user)
        db.session.commit()
        msg = Message("Password for HosteLite",
                sender="monagandhi09@gmail.com",
                recipients=["harshildoshi6333@gmail.com"])
        msg.body = "The password for your hostelite account is: "  + password + "\nPlease reset your password as soon as you login."      
        mail.send(msg)
        flash('Account created successfully.', 'success')

        return redirect(url_for('guard_list'))
        
    return render_template('admin/guard_create.html', form=form)

@app.route('/admin/guard/update/<int:id>' ,methods=['GET','POST'])
@login_required
def guard_update(id):
    user=User.query.get_or_404(id)
    form=UpdateMessStaffForm()

    if form.validate_on_submit():
        user.college_id = form.college_id.data
        user.firstname = form.firstname.data
        user.lastname = form.lastname.data
        user.address = form.address.data

        if form.password.data and form.confirm_password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            user.password = hashed_password

        db.session.commit()
        flash('Account information has been updated!', 'success')
        return redirect(url_for('guard_list'))

    elif request.method == 'GET':
        form.college_id.data = user.college_id
        form.firstname.data = user.firstname
        form.lastname.data = user.lastname
        form.address.data = user.address

    return render_template('admin/update_guard_info.html', title='Update', form=form, user=user)

@app.route('/admin/guard/delete/<int:id>' ,methods=['POST'])
@login_required
def guard_delete(id):
    user = User.query.get_or_404(id)
    announcements = Announcement.query.filter_by(user_id = id).delete()
    complaints = Complaint.query.filter_by(user_id = id).delete()
    answers = Answer.query.filter_by(user_id = id).delete()
    couriers = Courier.query.filter_by(user_id = id).delete()
    exitentries = ExitEntry.query.filter_by(user_id = id).delete()
    visitors = Visitor.query.filter_by(for_user_id = id).delete()

    db.session.delete(user)
    db.session.commit()
    flash('User successfully Deleted!', 'success')
    return redirect(url_for('guard_list'))

@app.route("/admin/complaints", methods=['GET','POST'])
@login_required
def complaint_list():
    complaints = Complaint.query.all()
    return render_template('admin/complaint_list.html', title='Complaints', complaints=complaints)



@app.route("/admin/complaints/<int:complaints>/status", methods=['GET','POST'])
@login_required
def complaint_status(complaints):
    complaint = Complaint.query.get_or_404(complaints)
    status = complaint.status
    if status == 'Unresolved':
        complaint.status = "Resolved"
    else:
        complaint.status = "Unresolved"

    print(complaint.status)
    db.session.commit()
    complaint = Complaint.query.get_or_404(complaints)
    print(complaint.status)
    return redirect(url_for('complaint_list'))

@app.route("/admin/announcements")
@login_required
def announcement_list():
    announcements = Announcement.query.all()
    return render_template('admin/announcement_list.html', title = 'Announcements', announcements = announcements)

@app.route("/admin/announcements/<int:announcement_id>")
def announcement_detail(announcement_id):
    user = current_user
    single_announcement = Announcement.query.get_or_404(announcement_id)
    return render_template('admin/announcement_detail.html', title=single_announcement.title, single_announcement=single_announcement, user=user)

@app.route("/admin/announcements/new", methods=['GET', 'POST'])
@login_required
def announcement_create():
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement = Announcement(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(announcement)
        db.session.commit()
        flash('Your announcement has been successfully published!', 'success')
        return redirect(url_for('announcement_list'))
    return render_template('admin/create_announcement.html', title='New Announcement', form = form, legend = 'Create New Announcement')

@app.route("/admin/announcements/<int:announcement_id>/update", methods=['GET', 'POST'])
@login_required
def announcement_update(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    form = AnnouncementForm()
    if form.validate_on_submit():
        announcement.title = form.title.data
        announcement.content = form.content.data
        db.session.commit()
        flash('Your announcement has been updated!', 'success')
        return redirect(url_for('announcement_list', announcement_id=announcement.id))
    elif request.method == 'GET':
        form.title.data = announcement.title
        form.content.data = announcement.content
    return render_template('admin/create_announcement.html', title='Update', form=form, legend = 'Update Announcement')


@app.route("/admin/announcements/<int:announcement_id>/delete", methods=['POST'])
@login_required
def announcement_delete(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    flash('Your announcement has been deleted!', 'success')
    return redirect(url_for('announcement_list'))