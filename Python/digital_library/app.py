from flask import Flask, render_template, request, redirect, url_for, flash
import os
from data_models import db, Author, Book
from flask_migrate import Migrate

app = Flask(__name__)

# Configuration
base_dir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'data/library.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize db and Migrate with the application
db.init_app(app)
migrate = Migrate(app, db)

# Create database
with app.app_context():
    db.create_all()


# Route for the home page with sorting and search
@app.route('/home')
def home():
    sort_by = request.args.get('sort_by', 'title')
    search_query = request.args.get('search_query', '')

    if sort_by == 'author':
        books = Book.query.join(Author).filter(Book.title.ilike(f'%{search_query}%')).order_by(Author.name,
                                                                                               Book.title).all()
    elif sort_by == 'publication_year':
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).order_by(Book.publication_year,
                                                                                  Book.title).all()
    else:
        books = Book.query.filter(Book.title.ilike(f'%{search_query}%')).order_by(Book.title).all()

    return render_template('home.html', books=books, sort_by=sort_by, search_query=search_query)


# Route for deleting a book
@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)

    # Check if the author has other books
    if not Book.query.filter_by(author_id=author.id).all():
        db.session.delete(author)

    db.session.commit()
    flash('Book deleted successfully!', 'success')
    return redirect(url_for('home'))


# Route for the main page
@app.route('/')
def index():
    return render_template('index.html')


# Route for searching books
@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('query', '')
    results = Book.query.filter(Book.title.ilike(f'%{query}%')).all()
    return render_template('search_results.html', results=results)


# Route for adding an author
@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        name = request.form['name']
        birth_date = request.form['birth_date']
        date_of_death = request.form['date_of_death']
        new_author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
        db.session.add(new_author)
        db.session.commit()
        flash('Author added successfully!', 'success')
        return redirect(url_for('add_author'))
    return render_template('add_author.html')


# Route for adding a book
@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        title = request.form['title']
        publication_year = request.form['publication_year']
        author_id = request.form['author_id']
        new_book = Book(title=title, publication_year=publication_year, author_id=author_id)
        db.session.add(new_book)
        db.session.commit()
        flash('Book added successfully!', 'success')
        return redirect(url_for('add_book'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


if __name__ == '__main__':
    app.run(debug=True)


