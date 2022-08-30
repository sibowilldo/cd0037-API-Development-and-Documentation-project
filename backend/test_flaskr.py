import os
import unittest
import json
from flaskr import create_app
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Question, Category

from dotenv import load_dotenv

load_dotenv()


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""
    new_question = {"question": "How tall is mount everest?", "answer": "8.8KM", "category": 3, "difficulty": 3}
    quiz_question = {"previous_questions": [15, 24, 25], "quiz_category": 3}

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client

        self.db_name = os.getenv("TEST_DB_DATABASE")
        self.db_user = os.getenv("TEST_DB_USER")
        self.db_password = os.getenv("TEST_DB_PASSWORD")
        self.db_host = f"{os.getenv('TEST_DB_HOST')}:{os.getenv('TEST_DB_PORT')}"

        self.database_path = f'postgresql://{self.db_user}:{self.db_password}@{self.db_host}/{self.db_name}'

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    def test_get_categories_route_return_categories(self):
        response = self.client().get("/api/v1/categories")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])

    def test_get_questions_returns_list_of_paginated_questions(self):
        response = self.client().get("/api/v1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["categories"])
        self.assertTrue(data["current_category"])
        self.assertTrue(data["total_questions"])
        self.assertTrue(data["questions"])

    def test_get_questions_returns_404_if_pagination_out_of_range(self):
        response = self.client().get("/api/v1/questions?page=10")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_delete_question_route_deletes_resource(self):
        question_id = 5

        response = self.client().delete(f"/api/v1/questions/{question_id}")
        data = json.loads(response.data)

        deleted_question = Question.query.filter(Question.id == question_id).first()

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["deleted_question"])
        self.assertEqual(deleted_question, None)

    def test_delete_question_route_returns_404_if_resource_is_not_available(self):
        question_id = 250

        response = self.client().delete(f"/api/v1/questions/{question_id}")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_search_question_route_returns_list_of_questions(self):
        response = self.client().post("/api/v1/questions", json={"searchTerm": "title"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], None)
        self.assertGreater(data["total_questions"], 0)
        self.assertGreater(len(data["questions"]), 0)

    def test_search_question_route_returns_no_questions(self):
        response = self.client().post("/api/v1/questions", json={"searchTerm": "no questions with this phrase"})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["current_category"], None)
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_create_new_question(self):
        response = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 201)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["message"], "Question saved!")

    def test_create_new_question_return_405_if_not_creation_not_allowed(self):
        response = self.client().post("/api/v1/questions/2", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_create_new_question_return_422_if_fields_are_not_acceptable(self):
        self.new_question["category"] = "Not a Number"

        response = self.client().post("/api/v1/questions", json=self.new_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_get_questions_by_category(self):
        response = self.client().get("/api/v1/categories/1/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"])
        self.assertEqual(data["total_questions"], len(data["questions"]))
        self.assertTrue(data["questions"])

    def test_get_questions_by_category_with_no_questions_in_category(self):
        response = self.client().get("/api/v1/categories/13/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["current_category"])
        self.assertEqual(data["total_questions"], 0)
        self.assertEqual(len(data["questions"]), 0)

    def test_get_questions_by_category_return_404_if_category_is_unacceptable(self):
        response = self.client().get("/api/v1/categories/13Z/questions")
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_play_quiz_any_random_question_in_category_but_not_in_previous_questions(self):
        response = self.client().post("/api/v1/quizzes", json=self.quiz_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertEqual(self.quiz_question["quiz_category"], data["question"]["category"])
        self.assertNotIn(data["question"]["category"], self.quiz_question["previous_questions"])

    def test_play_quiz_returns_any_random_question_if_category_doesnt_exit(self):
        quiz_question = self.quiz_question
        quiz_question["quiz_category"] = 100

        response = self.client().post("/api/v1/quizzes", json=quiz_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])
        self.assertNotEqual(quiz_question["quiz_category"], data["question"]["category"])

    def test_play_quiz_returns_any_random_question_if_category_not_supplied(self):
        response = self.client().post("/api/v1/quizzes",
                                      json={"previous_questions": self.quiz_question["previous_questions"]})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["question"])

    def test_play_quiz_returns_404_if_all_questions_in_category_are_in_previous_questions(self):
        category = Category.query.first().id
        questions = Question.query.filter(Question.category == category).all()
        questions = list(map(lambda q: q.id, questions))

        response = self.client().post("/api/v1/quizzes",
                                      json={"previous_questions": questions, "quiz_category": category})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])

    def test_play_quiz_returns_422_if_category_is_no_acceptable(self):
        quiz_question = self.quiz_question
        quiz_question["quiz_category"] = "Not a Number"

        response = self.client().post("/api/v1/quizzes", json=quiz_question)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
