from flask import Flask, request, render_template, redirect, url_for
from sqlalchemy import or_
from data_models import db, Author, Book
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/ASUS/PycharmProjects/pythonProject7/Book-Alchemy/data/library.sqlite'
db.init_app(app)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """Route renders template with form for adding new author, data from form saves to database."""
    if request.method == 'POST':
        author_name = request.form.get('name')
        birthdate = datetime.strptime(request.form.get('birthdate'), '%Y-%m-%d').date()
        date_of_death = datetime.strptime(request.form.get('date_of_death'), '%Y-%m-%d').date()
        author = Author(author_name=author_name, birth_date=birthdate, date_of_death=date_of_death)
        db.session.add(author)
        db.session.commit()
        return 'Author was added successfully'
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """Route renders template with form for adding new book, data from form saves to database."""
    #  Retrieve authors data for choosing book author from dropdown.
    authors = db.session.execute(db.select(Author)).all()

    if request.method == 'POST':
        isbn = request.form.get('isbn')
        title = request.form.get('title')
        author_id = request.form.get("author")
        publication_year = request.form.get('publication_year')
        book = Book(isbn=isbn, title=title, author=author_id, publication_year=publication_year)
        db.session.add(book)
        db.session.commit()
        return 'Book was added successfully'
    return render_template('add_book.html', authors=authors)


@app.route('/')
def home():
    """Route renders main page template with all books data tht stored in database."""
    books = db.session.execute(db.select(Book, Author).filter(Book.author == Author.author_id).order_by(Book.author))\
        .all()
    return render_template('home.html', books=books)


@app.route('/books_filtered_by_title')
def books_filtered_by_title():
    """Route for sorting books on the home page by title."""
    books = db.session.execute(db.select(Book, Author).filter(Book.author == Author.author_id).order_by(Book.title))\
        .all()
    return render_template('home.html', books=books)


@app.route('/books_filtered_by_author')
def books_filtered_by_author():
    """Route for sorting books on the home page by author."""
    books = db.session.execute(db.select(Book, Author).filter(Book.author == Author.author_id).\
                               order_by(Author.author_name)).all()
    return render_template('home.html', books=books)


@app.route('/search', methods=['GET', 'POST'])
def search():
    """Route for searching books on the home page by title or author fragment."""
    if request.method == 'POST':
        query = request.form.get('query')
        books = db.session.execute(db.select(Book, Author).filter(Book.author == Author.author_id).\
        order_by(Author.author_name).filter(or_(Author.author_name.like(f'%{query}%'), Book.title.like(f'%{query}%'))))\
            .all()
        if not books:
            return 'Nothing found'
        return render_template('home.html', books=books)


@app.route('/book/<int:book_id>/delete')
def delete_book(book_id):
    """Route for deleting book from database by its id number."""
    db.session.execute(db.delete(Book).filter_by(book_id=book_id))
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)


# with app.app_context():
#     db.create_all()
