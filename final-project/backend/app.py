import os
from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_mail import Mail, Message
from datetime import datetime

app = Flask(__name__)

# Ensure database directory exists
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DB_DIR = os.path.join(BASE_DIR, "../data")  # Database stored outside backend folder
os.makedirs(DB_DIR, exist_ok=True)

# Database Configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{os.path.join(DB_DIR, 'task_manager.db')}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "supersecretkey"

# Initialize database and encryption
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# Configure Flask-Mail (for task reminders)
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_email_password"
app.config["MAIL_USE_TLS"] = True
mail = Mail(app)

# Ensure upload folder exists
app.config["UPLOAD_FOLDER"] = os.path.join(BASE_DIR, "static/uploads")
os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

from models import User, Task  # Import models after initializing db

@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if user exists
        user = User.query.filter_by(username=username).first()

        if not user:
            return render_template("login.html", error="❌ Username does not exist!")

        # Check password
        if not user.check_password(password):
            return render_template("login.html", error="❌ Incorrect password!")

        # Successful login
        session["user_id"] = user.id
        return redirect(url_for("tasks"))

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]

        # Check if username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return render_template("register.html", error="❌ Username already exists!")

        # Check if email already exists
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return render_template("register.html", error="❌ Email already registered! Try logging in.")

        # Create new user
        new_user = User(username=username, email=email)
        new_user.set_password(password)

        # Add user to database
        db.session.add(new_user)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            return render_template("register.html", error="❌ An error occurred. Please try again.")

        return redirect(url_for("login", success="✅ Registration successful! Please log in."))

    return render_template("register.html")

@app.route("/tasks", methods=["GET", "POST"])
def tasks():
    if "user_id" not in session:
        return redirect(url_for("login"))

    user_id = session["user_id"]

    if request.method == "POST":
        title = request.form["title"]
        due_date_str = request.form["due_date"]
        priority = request.form["priority"]
        category = request.form["category"]
        attachment = request.files.get("attachment")

        # Convert string to datetime object
        due_date = datetime.strptime(due_date_str, "%Y-%m-%d") if due_date_str else None

        # Handle file attachment
        attachment_filename = None
        if attachment and attachment.filename:
            attachment_filename = os.path.join(app.config["UPLOAD_FOLDER"], attachment.filename)
            attachment.save(attachment_filename)

        new_task = Task(
            title=title,
            due_date=due_date,
            priority=priority,
            category=category,
            user_id=user_id,
            attachment=attachment_filename,
        )
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.priority.desc()).all()
    return render_template("tasks.html", tasks=tasks)

@app.route("/task/complete/<int:task_id>")
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
    return "", 204  # Send empty response (handled via JavaScript)

@app.route("/task/delete/<int:task_id>", methods=["GET"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return redirect(url_for("tasks"))
    return "Task not found", 404

@app.route("/task/clear", methods=["GET"])
def clear_tasks():
    try:
        num_deleted = Task.query.delete()  # Delete all tasks
        db.session.commit()
        return redirect(url_for("tasks"))
    except Exception as e:
        db.session.rollback()
        return f"Error clearing tasks: {str(e)}", 500

@app.route("/send_reminder/<int:task_id>")
def send_reminder(task_id):
    task = Task.query.get(task_id)
    user = User.query.get(task.user_id)

    if task and user:
        msg = Message(
            "Task Reminder",
            sender="your_email@gmail.com",
            recipients=[user.email]
        )
        msg.body = f"Reminder: {task.title} is due on {task.due_date}."
        mail.send(msg)

    return redirect(url_for("tasks"))

@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
