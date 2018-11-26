from app import app
from models import Message
import unittest
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy(app)

# class MessageController(unittest.TestCase):

#     def create_app(self):
#         app.config[
#             "SQLALCHEMY_DATABASE_URI"] = 'postgres://localhost/warbler_db_test'
#         return app

#      <div class="message-area">

# if __name__ == '__main__':
#     unittest.main()
