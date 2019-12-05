from flask import request, jsonify
from models import db
from models import Tasks, Project, User


def get_task():
    return jsonify({'Tasks': Tasks.query.all()})


def create_task():
    if request:
        try:
            # project = request.json.get('project', '')
            title = request.json.get('task_title', '')
            status = request.json.get('status', '')
            reason = request.json.get('reason', '')
            # user = request.json.get('user', '')
            # user_id = User.query.filter_by(user_name=user).user_id
            user_id = 1
            # project_id = Project.query.filter_by(project_name=project).project_id
            project_id = 1
            task = Tasks(task_title=title, status=status, reason=reason, project_id=project_id, user_id=user_id)
            db.session.add(task)
            db.session.commit()
            return jsonify({'Task': task})
        except Exception as e:
            print("couldn't store task", e)
        return jsonify({'Task': ''})


def update_task(id):
    task = Tasks.query.get(id)
    project = request.json.get('project', task.project)
    task.title = request.json.get('task_title', task.title)
    task.status = request.json.get('status', task.status)
    task.reason = request.json.get('reason', task.reason)
    user = request.json.get('user', task.user)
    task.user_id = User.query.filter_by(user_name=user).user_id
    task.project_id = Project.query.filter_by(project_name=project).project_id
    db.session.commit()
    return jsonify({'Task': task})


def delete_task(id):
    task = Tasks.query.get(id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'result': True})
