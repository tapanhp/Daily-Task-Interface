from app import db
import enum
import datetime


class Project(db.Model):
    project_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    project_name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Tasks', backref="project")


class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Tasks', backref="user")


class TaskStatusEnum(enum.Enum):
    green = "Green"
    yellow = "yellow"
    red = "red"


class Tasks(db.Model):
    task_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    task_title = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.Enum(TaskStatusEnum), nullable=False)
    reason = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
