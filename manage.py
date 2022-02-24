# built-in imports

# external imports
from flask.cli import FlaskGroup

# internal imports
from codeapp import bcrypt, create_app, db
from codeapp.models import User

app = create_app()
cli = FlaskGroup(create_app=create_app)  # type: ignore


@cli.command("initdb")  # type: ignore
def initdb() -> None:
    with app.app_context():
        db.drop_all()
        db.create_all()
        pwd = bcrypt.generate_password_hash("testing").decode("utf-8")
        default_1 = User(
            name="Default User",
            email="default@chalmers.se",
            password=pwd,
        )
        db.session.add(default_1)
        db.session.commit()


if __name__ == "__main__":
    cli()
