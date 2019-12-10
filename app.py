import json
import os
import flask
import google_auth
from flask import render_template

app = flask.Flask(__name__)
app.secret_key = "b']\xa0\x02\x94Rl\x15\x10z\x19\xdaEE\xbf\x08!'"
app.register_blueprint(google_auth.app)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "daily_tasks.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

from views import create_task, get_task, get_all_tasks, update_task, delete_task, get_all_projects, create_project, \
    delete_project, create_user, generate_report


@app.route('/')
def index():
    if google_auth.is_logged_in():
        response = create_user()
        response = json.loads(response.get_data())
        if response['status']:
            return render_template('tables.html')
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/tasks/', methods=['GET'])
def get_tasks():
    return get_all_tasks()


@app.route('/task/<int:user_id>/', methods=['GET'])
def get_task_main(user_id):
    return get_task(user_id)


@app.route('/task/', methods=["POST"])
def create_task_main():
    return create_task()


@app.route('/task/<int:task_id>/', methods=['PUT'])
def update_task_main(task_id):
    return update_task(task_id)


@app.route("/task/<int:task_id>/", methods=["DELETE"])
def delete_task_main(task_id):
    return delete_task(task_id)


@app.route("/project/", methods=["GET"])
def get_projects():
    return get_all_projects()


@app.route('/project/', methods=["POST"])
def create_project_main():
    return create_project()


@app.route("/project/<int:project_id>/", methods=["DELETE"])
def delete_project_main(project_id):
    return delete_project(project_id)


@app.route("/report/", methods=["GET", "POST"])
def generate_report_main():
    return generate_report()
