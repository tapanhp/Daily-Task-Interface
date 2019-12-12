import datetime
from flask_sqlalchemy import SQLAlchemy
from marshmallow import fields

from app import app
from flask_marshmallow import Marshmallow

db = SQLAlchemy(app)
ma = Marshmallow(app)

projects = db.Table('projects',
                    db.Column('project_id', db.Integer, db.ForeignKey('project.project_id'), primary_key=True),
                    db.Column('user_id', db.Integer, db.ForeignKey('user.user_id'), primary_key=True),
                    db.PrimaryKeyConstraint('project_id', 'user_id')
                    )


class Project(db.Model):
    project_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String(50), unique=True, nullable=False)
    tasks = db.relationship('Tasks', backref="project")

    def __str__(self):
        return self.project_name


class User(db.Model):
    user_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String(50), unique=True, nullable=False)
    user_email = db.Column(db.String(50), unique=True, nullable=False)
    is_admin = db.Column(db.Boolean, unique=False, default=False)
    tasks = db.relationship('Tasks', backref="user")
    projects = db.relationship('Project', secondary=projects, lazy='subquery',
                               backref=db.backref('projects', lazy=True), passive_deletes='all')

    def __str__(self):
        return self.user_name


class Tasks(db.Model):
    task_id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True, autoincrement=True)
    task_title = db.Column(db.String(500), unique=True, nullable=False)
    status = db.Column(db.String, nullable=False)
    reason = db.Column(db.Text, nullable=True)
    date = db.Column(db.Date, default=datetime.datetime.utcnow().date(), onupdate=datetime.datetime.utcnow().date())
    project_id = db.Column(db.Integer, db.ForeignKey('project.project_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)

    def __str__(self):
        return self.task_title


class ProjectSchema(ma.ModelSchema):
    class Meta:
        model = Project
        sqla_session = db.session
        fields = ('project_id', 'project_name')


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User
        sqla_session = db.session
        fields = ('user_id', 'user_name')


class TaskSchema(ma.ModelSchema):
    class Meta:
        model = Tasks
        sqla_session = db.session

    project = fields.Nested(ProjectSchema)
    user = fields.Nested(UserSchema)
