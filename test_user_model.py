from app import app
from models import User
import unittest
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class UserModelAttributes(unittest.TestCase):
    def create_app(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_db_test'
        return app

    def setUp(self):
        db.create_all()
        user1 = User(
            email="itsfriday@hotmail.com", username="tgif", password="123fish")
        user2 = User(
            email="kristenrules@hotmail.com",
            username="bayareababe",
            password="456easypeezy")
        user3 = User(
            email="kelleyisaditz@hotmail.com",
            username="tetonchick",
            password="474646574584ok")
        db.session.add_all([user1, user2, user3])
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_create_User(self):
        found_user = User.query.filter_by(username="tgif")
        self.assertIsNotNone(found_user)


if __name__ == '__main__':
    unittest.main()