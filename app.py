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


@app.route('/')
def index():
    if google_auth.is_logged_in():
        user_info = google_auth.get_user_info()
        return '<div>You are currently logged in as ' + user_info['given_name'] + '<div><pre>' + json.dumps(user_info,
                                                                                                            indent=4) \
               + "</pre>"

    return render_template('login.html')


from views import create_task, read_task, update_task


@app.route('/task/', methods=['GET'])
def get():
    return read_task()


@app.route('/task/', methods=["POST"])
def create():
    return create_task()


@app.route('/task/<int:id>', methods=['PUT'])
def update(id):
    return update_task(id)


# @app.route("/task/<int:id>", methods=["DELETE"])
# def delete(id):
#     return delete_task(id)
