from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
    """Class for creating authors table."""
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    author_name = db.Column(db.String)
    birth_date = db.Column(db.Date)
    date_of_death = db.Column(db.Date)


class Book(db.Model):
    """Class for creating books table."""
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title = db.Column(db.String)
    author = db.Column(db.Integer, db.ForeignKey('author.author_id'))
    publication_year = db.Column(db.Integer)



