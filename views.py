from flask import redirect
from flask import render_template
from flask import request
from app import app
from models import db
from models import Tasks, Project, User


@app.route('/form', methods=["GET", "POST"])
def create_task():
    if request.form:
        try:
            project = request.form.get('project')
            title = request.form.get('task_title')
            status = request.form.get('status')
            reason = request.form.get('reason')
            user = request.form.get('user')
            user_id = User.query.filter_by(user_name=user)
            project_id = Project.query.filter_by(project_name=project)
            task = Tasks(task_title=title, status=status, reason=reason, project_id=project_id, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            # return re
        except Exception as e:
            print("couldn't store task", e)
    return render_template("login.html")

