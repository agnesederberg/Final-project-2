from flask_login import current_user
from flask_wtf import FlaskForm
from sqlalchemy import select
from wtforms.fields import (
    BooleanField,
    EmailField,
    PasswordField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError

from codeapp import bcrypt, db
from codeapp.models import User

# useful links:
# always prefer HTML5 fields if an specific one exists
# WTForms fields: https://wtforms.readthedocs.io/en/3.0.x/fields/
# WTForms validators: https://wtforms.readthedocs.io/en/3.0.x/validators/


class LoginForm(FlaskForm):
    email = EmailField(
        "E-mail",
        validators=[
            # this field must be filled
            DataRequired(),
            # this field must have at least 5 characters
            Length(min=5),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            # this field must be filled
            DataRequired(),
            # this field needs to have at least 5 characters
            Length(min=5),
        ],
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class RegistrationForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            # this field must be filled
            DataRequired(),
            # the name must have 2-20 characters
            Length(min=2, max=128),
        ],
    )
    email = EmailField(
        "Email",
        validators=[
            # the user must fill this field
            DataRequired(),
            # validate as an email
            Email(),
        ],
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=2, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            # user must fill the `confirm password`
            DataRequired(),
            # the value here must be equal to the `password`
            EqualTo("password"),
        ],
    )
    submit = SubmitField("Sign Up")

    def validate_email(self, email: EmailField) -> None:
        _stmt = select(User).filter(User.email == email.data).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        if _user:
            # if a user exists with this email,
            # you cannot create a second user using it.
            # By raising an error, the message is shown to the user.
            raise ValidationError(
                "This email is already registered. " "Please choose a different one."
            )


class UpdateProfileForm(FlaskForm):
    name = StringField(
        "Name",
        validators=[
            # this field must be filled
            DataRequired(),
            # the name must have 2-20 characters
            Length(min=2, max=20),
        ],
    )
    # name needs to be different given that we have two forms in one page
    submit_profile = SubmitField("Update Profile")


class UpdatePasswordForm(FlaskForm):
    current_password = PasswordField(
        "Current Password", validators=[DataRequired(), Length(min=2, max=20)]
    )
    new_password = PasswordField(
        "New Password", validators=[DataRequired(), Length(min=2, max=20)]
    )
    confirm_password = PasswordField(
        "Confirm New Password",
        validators=[
            # user must fill the `confirm password`
            DataRequired(),
            Length(min=2, max=20),
            # the value here must be equal to the `password`
            EqualTo("new_password"),
        ],
    )
    # name needs to be different given that we have two forms in one page
    submit_password = SubmitField("Change Password")

    def validate_current_password(self, current_password: PasswordField) -> None:
        _stmt = select(User).filter(User.id == current_user.id).limit(1)
        _user = db.session.execute(_stmt).scalars().first()
        if not bcrypt.check_password_hash(_user.password, current_password.data):
            raise ValidationError(
                "Your current password did not match! "
                "Please input the right password."
            )
