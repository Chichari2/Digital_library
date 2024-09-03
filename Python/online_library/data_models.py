from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Author(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  birth_date = db.Column(db.String(10))  # Adjust as needed for date format
  date_of_death = db.Column(db.String(10))  # Adjust as needed for date format

  def __repr__(self):
    return f'<Author {self.name}>'

  def __str__(self):
    return self.name


class Book(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  isbn = db.Column(db.String(13))  # Optional, adjust length as needed
  title = db.Column(db.String(100), nullable=False)
  publication_year = db.Column(db.Integer)
  author_id = db.Column(db.Integer, db.ForeignKey('author.id'), nullable=False)

  author = db.relationship('Author', backref=db.backref('books', lazy=True))

  def __repr__(self):
    return f'<Book {self.title}>'

  def __str__(self):
    return self.title
