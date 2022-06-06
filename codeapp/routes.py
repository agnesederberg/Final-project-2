# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
"""

import json
from typing import Union

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    render_template,
    request,
    url_for,
)
from flask.wrappers import Response as FlaskResponse
from flask_login import current_user, login_required, login_user, logout_user
from sqlalchemy import select
from werkzeug.wrappers.response import Response as WerkzeugResponse

# app imports
from codeapp import bcrypt, db
from codeapp.forms import (
    LoginForm,
    RegistrationForm,
    UpdatePasswordForm,
    UpdateProfileForm,
)
from codeapp.models import Category, Folder, Note, User

Response = Union[str, FlaskResponse, WerkzeugResponse]

bp = Blueprint("bp", __name__, url_prefix="/")

"""
############################### General routes ################################

The routes below include general views open for all users.
"""


@bp.get("/")
def home() -> Response:
    return render_template("home.html")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


"""
########################## Specific project routes ############################

Add here the routes specific to your project.
"""


@bp.route("/folders", methods=["GET", "POST"])
@login_required
def folders() -> Response:
    category = db.session.query(Category)

    if request.method == "POST":
        folder: str = request.form.get("folder")
        category = request.form.get("category")

        new_folder = Folder(
            name=folder, category_id=int(category), user_id=current_user.id
        )
        db.session.add(new_folder)
        db.session.commit()
        flash("Folder added!", category="success")
        category = db.session.query(Category)

    return render_template("folders.html", user=current_user, category=category)


@bp.route("/delete-folder", methods=["POST", "GET"])
def delete_folder() -> Response:
    category = db.session.query(Category)
    folder = json.loads(request.data)
    print(request.data)
    folder_id = folder["folderId"]
    folder = db.session.query(Folder).filter(Folder.id == folder_id).one()
    if folder:
        db.session.delete(folder)
        db.session.commit()
        flash("Folder deleted!", category="success")

    return render_template("folders.html", user=current_user, category=category)


@bp.route("/delete-note", methods=["POST"])
@login_required
def delete_note() -> Response:
    note = json.loads(request.data)
    note_id = note["noteId"]
    note = db.session.query(Note).filter(Note.id == note_id).first()
    folder = db.session.query(Folder).filter(Folder.id == note.folder_id).first()
    if note:
        db.session.delete(note)
        db.session.commit()
        flash("Note deleted!", category="success")

    return render_template("notes.html", user=current_user, folder=folder)


@bp.route("/folders/<int:folder_id>", methods=["POST", "GET"])
def note_view(folder_id: int) -> Response:
    folder = db.session.query(Folder).filter(Folder.id == folder_id).first()
    search = None

    if request.method == "POST":
        if request.form["submit"] == "addNote":
            note = request.form.get("note")
            new_note = Note(data=note, folder_id=folder.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note added!", category="success")
        elif request.form["submit"] == "search":
            search = request.form.get("search")
        elif request.form["submit"] == "clearSearch":
            search = None

    return render_template(
        "notes.html", folder=folder, user=current_user, search=search
    )


"""
############################ User-related routes ##############################

The routes below include routes related to the user.
"""


@bp.route("/register", methods=["GET", "POST"])
def register() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("bp.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        _password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        _user = User(name=form.name.data, email=form.email.data, password=_password)
        db.session.add(_user)
        try:
            db.session.commit()
            flash("User successfully created. Please log in!", "success")
            return redirect(url_for("bp.login"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while creating your user. Please try again later.",
                "danger",
            )
    return render_template("register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login() -> Response:
    if current_user.is_authenticated:
        return redirect(url_for("bp.home"))
    form = LoginForm()
    if form.validate_on_submit():
        _stmt = select(User).filter(User.email == form.email.data).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        current_app.logger.debug(f"User ({type(_user)}): {_user}")
        if _user and bcrypt.check_password_hash(_user.password, form.password.data):
            login_user(_user, remember=form.remember.data)
            next_page = request.args.get("next")
            flash("Welcome!", "success")
            if next_page:
                return redirect(next_page)
            return redirect(url_for("bp.home"))
        flash("Login Unsuccessful. Please check email and password.", "danger")
    return render_template("login.html", title="Login", form=form)


@bp.get("/logout")
def logout() -> Response:
    logout_user()
    flash("Logout successful!", "success")
    return redirect(url_for("bp.login"))


@bp.get("/profile")
@login_required
def profile() -> Response:
    return render_template("profile.html")


@bp.route("/update_profile", methods=["GET", "POST"])
@login_required
def update_profile() -> Response:
    profile_form = UpdateProfileForm()
    password_form = UpdatePasswordForm()

    if profile_form.validate_on_submit():
        current_app.logger.info("profile form submitted")
        _stmt = select(User).filter(User.id == current_user.id).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        _user.name = profile_form.name.data
        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            current_app.logger.info("Profile updated successfully")
            return redirect(url_for("bp.profile"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while updating your profile. "
                "Please try again later.",
                "danger",
            )

    if password_form.validate_on_submit():
        # user tried to update its password
        # if it gets here, it's because the current password is validated
        # new password and confirmation are also equal
        # see forms.py for more info
        _new_password = bcrypt.generate_password_hash(
            password_form.new_password.data
        ).decode("utf-8")
        _stmt = select(User).filter(User.id == current_user.id).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        _user.password = _new_password
        try:
            db.session.commit()
            current_app.logger.info("Password changed successfully.")
            flash(
                "Password updated successfully! Log in with your new password!",
                "success",
            )
            logout_user()
            return redirect(url_for("bp.login"))
        except Exception as e:
            current_app.logger.exception(e)
            db.session.rollback()
            flash(
                "There was an error while updating your password. "
                "Please try again later.",
                "danger",
            )

    # filling the form with the current data
    profile_form.name.data = current_user.name

    return render_template(
        "update_profile.html",
        profile_form=profile_form,
        password_form=password_form,
    )
