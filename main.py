from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import sqlite3

# create the extension
db = SQLAlchemy()
# create the app
app = Flask(__name__)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"
# initialize the app with the extension
db.init_app(app)


class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    author = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'


# Create table schema in the database after defining the models
with app.app_context():
    db.create_all()


def get_all_books():
    result = db.session.execute(db.select(Book).order_by(Book.title))
    all_books = result.scalars().fetchall()
    return all_books


@app.route("/home")
@app.route('/')
def home():
    all_books = get_all_books()
    print(all_books)
    print(type(all_books))
    return render_template("index.html", books=all_books)


@app.route("/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        book = request.form.get("book")
        author = request.form.get("author")
        rating = request.form.get("rating")
        new_book = Book(title=book, author=author, rating=rating)
        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html")


@app.route("/edit/<int:book_id>", methods=['GET', 'POST'])
def edit(book_id):
    book_to_update = db.get_or_404(Book, book_id)
    if request.method == 'POST':
        book_to_update.rating = request.form.get("rating")
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", book=book_to_update)


@app.route("/delete/<int:book_id>")
def delete(book_id):
    book_to_delete = db.get_or_404(Book, book_id)
    db.session.delete(book_to_delete)
    db.session.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
