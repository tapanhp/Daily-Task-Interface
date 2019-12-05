from flask import request, jsonify
from models import db
from models import Tasks, Project, User, TaskSchema, ProjectSchema, UserSchema


def read_task():
    task = Tasks.query.all()
    task_schema = TaskSchema(many=True)
    return jsonify(task_schema.dump(task).data)


def create_task():
    if request:
        try:
            task_schema = TaskSchema()
            task = task_schema.load(request.json, session=db.session).data
            db.session.add(task)
            db.session.commit()
            return jsonify(task_schema.dump(task).data)
        except Exception as e:
            print("couldn't store task", e)
            return jsonify({'Task': ''})


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
