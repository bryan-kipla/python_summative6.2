from faker import Faker
from models import db, User, Note
from app import create_app

fake = Faker()

app = create_app()
with app.app_context():
    # Clear existing data
    db.drop_all()
    db.create_all()

    # Create users
    users = []
    for i in range(5):
        user = User(username=fake.user_name(), email=fake.email())
        user.set_password("password123")
        db.session.add(user)
        users.append(user)
    db.session.commit()

    # Create notes for each user
    for user in users:
        for _ in range(3):
            note = Note(title=fake.sentence(), content=fake.text(), user_id=user.id)
            db.session.add(note)
    db.session.commit()

    print("Database seeded successfully!")
