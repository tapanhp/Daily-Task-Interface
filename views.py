from flask import request,render_template,jsonify
from app import app, db
from models import Tasks, Project, User


@app.route('/form', methods=["GET", "POST"])
def create_task():
    if request:
        try:
            project = request.json.get('project', '')
            title = request.json.get('task_title', '')
            status = request.json.get('status', '')
            reason = request.json.get('reason', '')
            user = request.json.get('user', '')
            user_id = User.query.filter_by(user_name=user).user_id
            project_id = Project.query.filter_by(project_name=project).project_id
            task = Tasks(task_title=title, status=status, reason=reason, project_id=project_id, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return jsonify({'Task': task})
        except Exception as e:
            print("couldn't store task", e)
    return render_template("login.html")

