from flask import Flask, render_template, redirect, request, g, session, url_for, flash
# from model import User, Post
# from flask.ext.login import LoginManager, login_required, login_user, current_user
# from flaskext.markdown import Markdown
import config
# import forms
# import model

app = Flask(__name__)
app.config.from_object(config)

# # Stuff to make login easier
# login_manager = LoginManager()
# login_manager.init_app(app)
# login_manager.login_view = "login"

# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(user_id)

# # End login stuff

# Adding markdown capability to the app


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
