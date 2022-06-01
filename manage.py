# built-in imports

# external imports
from flask.cli import FlaskGroup

# internal imports
from codeapp import bcrypt, create_app, db
from codeapp.models import Category, Folder, Note, User

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

        pwd = bcrypt.generate_password_hash("testing2").decode("utf-8")
        default_2 = User(
            name="Default User2",
            email="default2@chalmers.se",
            password=pwd,
        )
        db.session.add(default_2)
        db.session.commit()

        pwd = bcrypt.generate_password_hash("testing3").decode("utf-8")
        default_3 = User(
            name="Default User3",
            email="default3@chalmers.se",
            password=pwd,
        )
        db.session.add(default_3)
        db.session.commit()

        pwd = bcrypt.generate_password_hash("testing4").decode("utf-8")
        default_4 = User(
            name="Default User4",
            email="default4@chalmers.se",
            password=pwd,
        )
        db.session.add(default_4)
        db.session.commit()

        pwd = bcrypt.generate_password_hash("testing5").decode("utf-8")
        default_5 = User(
            name="Default User5",
            email="default5@chalmers.se",
            password=pwd,
        )
        db.session.add(default_5)
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

        horses = Folder(name="Horses", user_id=1, category_id=1)
        db.session.add(horses)
        db.session.commit()

        sudukogames = Folder(name="Suduko Games", user_id=1, category_id=1)
        db.session.add(sudukogames)
        db.session.commit()

        traveling = Folder(name="Traveling", user_id=1, category_id=1)
        db.session.add(traveling)
        db.session.commit()

        volvo = Folder(name="Volvo", user_id=1, category_id=1)
        db.session.add(volvo)
        db.session.commit()

        recipe = Folder(name="Recipe", user_id=1, category_id=1)
        db.session.add(recipe)
        db.session.commit()

        hast = Note(data="Go to the stables before july", folder_id=1)
        db.session.add(hast)
        db.session.commit()

        suduko = Note(data="complete games: 5/15", folder_id=2)
        db.session.add(suduko)
        db.session.commit()

        resor = Note(data="Book the plane to London and use the voucher", folder_id=3)
        db.session.add(resor)
        db.session.commit()

        bilar = Note(data="cars I want to buy", folder_id=4)
        db.session.add(bilar)
        db.session.commit()

        recept = Note(
            data="swedish pancakes: 1 egg, 1 dl flour, 2 dl milk", folder_id=5
        )
        db.session.add(recept)
        db.session.commit()


if __name__ == "__main__":
    cli()
