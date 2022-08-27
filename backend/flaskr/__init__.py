import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.exceptions import UnprocessableEntity, NotFound
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    """
    @DONE: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    """
    @DONE: Use the after_request decorator to set Access-Control-Allow
    """

    @app.after_request
    def after_request(response):
        response.headers.add("Access-Control-Allow-Headers", "Content-Type:, Authorization,True")
        response.headers.add("Access-Control-Allow-Methods", "GET,PUT,PATCH,POST,DELETE,OPTIONS")
        return response

    """
    @DONE:
    Create an endpoint to handle GET requests
    for all available categories.
    """

    @app.get("/api/v1/categories")
    def get_all_categories():
        categories = Category.query.all()
        categories = list(map(lambda category: category.format(), categories))
        return jsonify({"success": True,
                        "categories": categories})

    """
    @DONE:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.

    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """

    @app.route("/api/v1/questions")
    def get_all_questions():
        page = request.args.get("page", 1, int)
        questions = Question.query.order_by(Question.id).paginate(page=page, per_page=QUESTIONS_PER_PAGE,
                                                                  error_out=True)
        total_questions = questions.total
        questions = list(map(lambda question: question.format(), questions.items))

        categories = Category.query.all()
        categories = list(map(lambda category: category.format(), categories))

        return jsonify({"success": True,
                        "questions": questions,
                        "total_questions": total_questions,
                        "current_category": categories[0],
                        "categories": categories})

    """
    @DONE:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """

    @app.delete("/api/v1/questions/<int:question_id>")
    def delete_question_by_id(question_id):
        question = Question.query.filter(Question.id == question_id).first_or_404(description="Question not found.")
        question.delete()
        return jsonify({"success": True,
                        "deleted_question": question_id})

    """
    @DONE:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """

    """
    @DONE:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """

    @app.post('/api/v1/questions')
    def create_or_search_question():
        req = request.get_json()
        try:
            search_term = req.get("searchTerm", None)
            # If request has Search Term, assume it's a search request
            if search_term is not None:
                questions = Question.query.order_by(Question.id).filter(
                    Question.question.ilike(f'%{search_term}%')).all()
                questions = list(map(lambda q: q.format(), questions))
                return jsonify({"success": True,
                                "questions": questions,
                                "total_questions": len(questions),
                                "current_category": None})

            # Otherwise assume post is for new Question
            new_question = req.get("question", None)
            new_answer = req.get("answer", None)
            new_difficulty = req.get("difficulty", 1)
            new_category = req.get("category", None)
            question = Question(new_question, new_answer, new_category, new_difficulty)

            question.insert()

            return jsonify({"success": True, "message": "Question saved!"})
        except Exception:
            raise UnprocessableEntity

    """
    @DONE:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """

    @app.get('/api/v1/categories/<int:category_id>/questions')
    def get_questions_by_category(category_id):
        try:
            questions = Question.query.order_by(Question.id).filter(Question.category == category_id).all()
            questions = list(map(lambda question: question.format(), questions))

            return jsonify({"success": True,
                            "questions": questions,
                            "total_questions": len(questions),
                            "current_category": category_id})
        except Exception:
            raise UnprocessableEntity

    """
    @DONE:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """

    @app.post("/api/v1/quizzes")
    def quiz_question():
        req = request.get_json()
        prev_questions = req.get("previous_questions", [])
        category_id = req.get("quiz_category", None)
        try:
            # Let's first check if we have the whatever was passed as category_id
            # An exception will be raised if anything but a number is passed
            category = Category.query.filter(Category.id == category_id).first()
            # Let's return an unfiltered query if the category is None
            q = Question.query if category is None else Question.query.filter(Question.category == category.id)
            # Let's chain whatever query we got from above with a Not In [] filter, and get the results
            questions = q.filter(Question.id.not_in(prev_questions)).all()
            # Finally, let's pick a random item from the return results.
            # Will throw IndexError if results empty
            question = random.choice(questions)
            return jsonify({"success": True, "question": question.format()})
        except IndexError:
            raise NotFound(description="No questions found, that match your criteria")
        except Exception:
            raise UnprocessableEntity

    """
    @DONE:
    Create error handlers for all expected errors
    including 404 and 422.
    """

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"success": False, "status_code": 400, "message": "Bad request."}), 400

    @app.errorhandler(404)
    def resource_not_found(error):
        description = error.description if error.description else "Resource not found."
        return jsonify({"success": False, "status_code": 404, "message": description}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"success": False, "status_code": 405, "message": "Method not allowed."}), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({"success": False, "status_code": 422, "message": "Unprocessable entity."}), 422

    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({"success": False, "status_code": 429, "message": "Too many requests."}), 429

    @app.errorhandler(500)
    def too_many_requests(error):
        return jsonify({"success": False, "status_code": 500, "message": "Internal Server Error."}), 500

    return app
