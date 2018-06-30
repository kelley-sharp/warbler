from app import app, db, bcrypt
from models import User
from flask_testing import TestCase
import unittest
from flask_sqlalchemy import SQLAlchemy


class UserController(TestCase):
    def create_app(self):
        app.config[
            "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_db_test'
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        return app

    def setUp(self):
        db.create_all()
        password1 = bcrypt.generate_password_hash("password").decode('UTF-8')
        password2 = bcrypt.generate_password_hash("rithmrithm").decode('UTF-8')
        password3 = bcrypt.generate_password_hash("123fish").decode('UTF-8')
        user1 = User(
            email="itsfriday@hotmail.com", username="tgif", password=password1)
        user2 = User(
            email="kristenrules@hotmail.com",
            username="bayareababe",
            password=password2)
        user3 = User(
            email="kelleyisaditz@hotmail.com",
            username="tetonchick",
            password=password3)
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        self.client = app.test_client()

    def tearDown(self):
        db.session.close()
        db.drop_all()

    def login(self, username, password):
        return self.client.post(
            '/login',
            data=dict(username=username, password=password),
            follow_redirects=True)

    def logout(self):
        return self.client.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        result = self.login('tgif', 'password')
        # print(result.data)
        self.assertIn(b'Log out', result.data)
        # result = self.logout()
        # self.assertIn(b'You have successfully logged out.', result.data)
        # result = self.login('adminx', 'default')


if __name__ == '__main__':
    unittest.main()
