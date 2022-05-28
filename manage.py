# built-in imports

# external imports
from flask.cli import FlaskGroup

# internal imports
from codeapp import bcrypt, create_app, db
from codeapp.models import User, Category, Folder, Note

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

        work = Category(name="Work")
        db.session.add(work)
        db.session.commit()

        notwork = Category(name="Not Work")
        db.session.add(notwork)
        db.session.commit()

        freetime = Category(name="Free time")
        db.session.add(freetime)
        db.session.commit()

        school = Category(name="School")
        db.session.add(school)
        db.session.commit()

        memories = Category(name="Memories")
        db.session.add(memories)
        db.session.commit()

        blabla = Folder(name="Bla Bla", user_id=1, category_id=1)
        db.session.add(blabla)
        db.session.commit()



if __name__ == "__main__":
    cli()
