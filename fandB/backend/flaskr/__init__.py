import os
from flask import Flask, request, abort, jsonify
from models import setup_db, Book
from flask_cors import CORS
import random



BOOKS_PER_SHELF = 8

def paginate_books(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * BOOKS_PER_SHELF
    end = start + BOOKS_PER_SHELF
    
    books = [book.format() for book in selection]
    current_book = books[start:end]
    
    return current_book


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response
    
    @app.route('/status')
    def home():
        
        return jsonify({
            'status': 'ok',
            'response':'working',
            'code': 200
        })

    
    @app.route('/books/', methods=['GET','POST'])
    def get_books():
        selection = Book.query.order_by(Book.id).all()
        current_books = paginate_books(request, selection)
        
        return jsonify({
            'books': current_books,
            'success': True,
            'total_books': len(Book.query.all())
        })
    
    @app.route('/books/<int:book_id>', methods=['PATCH'])
    def update_books(book_id):
        
        body = request.get_json()
        
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            
            if book is None:
                abort(404)
            
            if 'rating' in body:
                book.rating = int(boody.get['rating'])
            
            book.update()
            
            return jsonify({
                'success': True
            })
        
        except:
            abort(404)
    
    
    @app.route('/books/<int:book_id>', methods=['DELETE'])
    def delete_book(book_id):
        
        try:
            book = Book.query.filter(Book.id == book_id).one_or_none()
            
            if book is None:
                abort(404)
            
            book.delete()
            
            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)
            
            return jsonify({
                'success': True,
                'deleted': book_id,
                'books': current_books,
                'book_length': len(Book.query.all())
            })
        
        except:
            abort(422)

   
    @app.route("/books", methods=["POST"])
    def create_book():
        body = request.get_json()

        new_title = body.get("title", None)
        new_author = body.get("author", None)
        new_rating = body.get("rating", None)

        try:
            book = Book(title=new_title, author=new_author, rating=new_rating)
            book.insert()

            selection = Book.query.order_by(Book.id).all()
            current_books = paginate_books(request, selection)

            return jsonify(
                {
                    "success": True,
                    "created": book.id,
                    "books": current_books,
                    "total_books": len(Book.query.all()),
                }
            )

        except:
            abort(422)

    @app.errorhandler(404)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 404, "message": "resource not found"}),
            404,
        )

    @app.errorhandler(422)
    def unprocessable(error):
        return (
            jsonify({"success": False, "error": 422, "message": "unprocessable"}),
            422,
        )

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    return app

if __name__ == "__main__":
    app=create_app()
    app.run(debug=True)