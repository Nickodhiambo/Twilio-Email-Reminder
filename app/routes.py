from flask import render_template, url_for, redirect, flash
from app import app, db
from app.forms import RegistrationForm, LoginForm, TaskForm
from app.email import send_reminder_email
from app.models import User, Task
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from app import scheduler


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(user)
        db.session.commit()
        flash('Account created successfully!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Login failed. Check email or password')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/task/new', methods = ['GET', 'POST'])
# @login_required
def new_task():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(title=form.title.data, description=form.description.data,
                    due_date=form.due_date.data, user_id=current_user.id)
        db.session.add(task)
        db.session.commit()
        send_reminder_email(current_user.email, task.title, task.due_date)
        flash('Task added successfully and reminder email sent')
        return redirect(url_for('dashboard'))
    return render_template('new_task.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', tasks=tasks)


def check_due_tasks():
    tasks = Task.query.filter_by(
        Task.due_date>=datetime.utcnow(),
        Task.due_date<=datetime.utcnow() + timedelta(hours=1),
        Task.reminder_sent==False
    ).all()

    for task in tasks:
        user = User.query.get(task.user_id)
        send_reminder_email(user.email, task.title, task.due_date)
        task.reminder_sent = True
        db.session.commit()

# Schedule the task checker to run every 10 minutes
scheduler.add_job(check_due_tasks, trigger="interval", minutes=10)