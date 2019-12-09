import datetime
from flask_sqlalchemy import SQLAlchemy

from app import app
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)

projects = db.Table('projects',
                    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
                    )


class Project(db.Model):
    project_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Tasks', backref="project")


class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    tasks = db.relationship('Tasks', backref="user")
    projects = db.relationship('Project', secondary=projects, lazy='subquery',
                               backref=db.backref('projects', lazy=True))


class Tasks(db.Model):
    task_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    task_title = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime(timezone=False), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        sqla_session = db.session
        fields = ('project_id', 'project_name')


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
        fields = ('user_id', 'user_name', 'user_email')


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Tasks
        sqla_session = db.session
        fields = ('task_id', 'task_title', 'status', 'reason', 'date', 'project', 'user')
