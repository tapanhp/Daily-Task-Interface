import json
import os
import flask
import google_auth
from flask import render_template, redirect, session

app = flask.Flask(__name__)
app.secret_key = "b']\xa0\x02\x94Rl\x15\x10z\x19\xdaEE\xbf\x08!'"
app.register_blueprint(google_auth.app)
project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "daily_tasks.db"))
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

from views import create_task, get_task, get_all_tasks, update_task, delete_task, get_all_projects, create_project, \
    delete_project, create_user, generate_report


def login_required(func):
    def wrapper(*args, **kwargs):
        if google_auth.is_logged_in():
            return func()
        return redirect("/")

    wrapper.__name__ = func.__name__
    return wrapper


@app.route('/')
def index():
    if google_auth.is_logged_in():
        response = create_user()
        context={
            'user_id':session['user'],
                 }
        response = json.loads(response.get_data())
        if response['status']:
            return render_template('tables.html',context=context)
        else:
            return render_template('login.html')
    return render_template('login.html')


@app.route('/tasks/', methods=['GET'])
# @login_required
def get_tasks():
    return get_all_tasks()


@app.route('/task/<int:user_id>/', methods=['GET'])
# @login_required
def get_task_main(user_id):
    return get_task(user_id)


@app.route('/task/', methods=["POST"])
# @login_required
def create_task_main():
    return create_task()


@app.route('/task/<int:task_id>/', methods=['PUT'])
@login_required
def update_task_main(task_id):
    return update_task(task_id)


@app.route("/task/<int:task_id>/", methods=["DELETE"])
#@login_required
def delete_task_main(task_id):
    return delete_task(task_id)


@app.route("/project/", methods=["GET"])
#@login_required
def get_projects():
    return get_all_projects()


@app.route('/project/', methods=["POST"])
#@login_required
def create_project_main():
    return create_project()


@app.route("/project/<int:project_id>/", methods=["DELETE"])
#@login_required
def delete_project_main(project_id):
    return delete_project(project_id)


@app.route("/report/", methods=["GET"])
@login_required
def generate_report_main():
    return generate_report()


@app.route("/table/")
def render_table():
    context = {
        'user_id': session['user'],
    }
    return render_template('tables.html',context=context)


@app.route("/admin/")
def render_admin():
    return render_template('admin.html')


@app.route("/create_task/")
def render_create():
    return render_template('create.html')


@app.route("/select/")
def render_select():
    return render_template('select.html')


@app.route("/edit/")
def render_edit():
    return render_template('edit.html')