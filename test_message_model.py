from app import app
from models import Message
import unittest
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)


class MessageModelAttributes(unittest.TestCase):
    def create_app(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_db_test'
        return app

    def setUp(self):
        db.create_all()
        message1 = Message(text="Hello Friday")
        message2 = Message(text="Harry Potter is awesome")
        message3 = Message(text="So is Star Wars")
        db.session.add_all([message1, message2, message3])
        db.session.commit()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def test_create_message(self):
        found_message = Message.query.filter_by(text="Hello Friday")
        self.assertIsNotNone(found_message)


if __name__ == '__main__':
    unittest.main()
