from flask import request, jsonify
from models import db
from models import Tasks, Project, User, TaskSchema, ProjectSchema, UserSchema
from response_utils import send_error_response, send_success_response


def read_task():
    try:
        task = Tasks.query.all()
        task_schema = TaskSchema(many=True)
        data = task_schema.dump(task).data
        message = "Successfully retrieved tasks"
        return send_success_response(message, data)
    except Exception as e:
        print(e)
        message = "Error in retrieving tasks"
        return send_error_response(message)


def create_task():
    if request:
        try:
            project = request.json.get('project')
            title = request.json.get('task_title')
            status = request.json.get('status')
            reason = request.json.get('reason')
            user = request.json.get('user')
            user_obj = User.query.filter_by(user_name=user).first()
            project_obj = Project.query.filter_by(project_name=project).first()
            task = Tasks(task_title=title, status=status, reason=reason, project=project_obj, user=user_obj)
            db.session.add(task)
            db.session.commit()
            message = "Successfully saved task"
            return send_success_response(message)
        except KeyError as e:
            print(e)
            return send_error_response()
        except Exception as e:
            print("couldn't store task", e)
            message = "Error in storing task"
            return send_error_response(message)


def update_task(id):
    try:
        task = Tasks.query.get(task_id=id)
        task.project_id = request.json.get('project', task.project_id)
        task.title = request.json.get('task_title', task.task_title)
        task.status = request.json.get('status', task.status)
        task.reason = request.json.get('reason', task.reason)
        task.user_id = request.json.get('user', task.user_id)
        db.session.commit()
        return jsonify({'Task': task})
    except Exception as e:
        print("not updated due to ", e)
        return jsonify("Task not updated")

# def delete_task(id):
#     task = Tasks.query.get(id)
#     db.session.delete(task)
#     db.session.commit()
#     return jsonify({'result': True})
