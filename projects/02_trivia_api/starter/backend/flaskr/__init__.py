import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    # Set up CORS. Allow '*' for all origins.
    cors = CORS(app, resources={
                '/*': {"origins": "*", "supports_credentials": True}})

    ''' Sets access control
  '''
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
  Handle GET requests for all available categories.
  '''

    @app.route('/categories')
    def get_categories():

        all_categories = {}
        categories = Category.query.all()
        for category in categories:
            all_categories[category.id] = category.type

        # abort 404 if no categories found
        if len(all_categories) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'categories': all_categories
        })

    '''
  utility for paginating questions
  '''

    def paginate_questions(request, selection):
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE

        questions = [question.format() for question in selection]
        current_questions = questions[start:end]
        return current_questions

    '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''

    '''
  Handle GET requests for all available questions.
  '''
    @app.route('/questions')
    def get_questions():

        # get all questions and paginate
        selection = Question.query.order_by(Question.id).all()
        current_questions = paginate_questions(request, selection)

        # get all categories and add to dict
        all_categories = {}
        categories = Category.query.all()
        for category in categories:
            all_categories[category.id] = category.type

           # abort 404 if no questions
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(selection),
            'categories': all_categories

        })

    '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''

    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):

        try:
            question = Question.query.filter(
                Question.id == question_id).one_or_none()
            # abort 404 if question does not exist
            if question is None:
                abort(404)

            question.delete()
            selection = Question.query.order_by(Question.id).all()
            # paginate based on current location
            paginate_questions(request, selection)

            return jsonify({
                'success': True,
                'total_questions': len(selection),
                'deleted': question_id

            })

        except:
            abort(422)

    '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''

    @app.route('/questions', methods=['POST'])
    def new_question():

        body = request.get_json()

        search = body.get('searchTerm', None)

        try:
            if search:
                selection = Question.query.order_by(Question.id).filter(
                    Question.question.ilike('%{}%'.format(search))).all()

                # abort if no results found
                if (len(selection) == 0):
                    abort(404)
                # paginate results
                paginate_question = paginate_questions(request, selection)

                return jsonify({
                    'success': True,
                    'questions': paginate_question,
                    'total_questions': len(Question.query.all()),
                    'current_category': ""
                })

            else:

                # if any does not exist we'll set to none
                question = body.get('question', None)
                answer = body.get('answer', None)
                category = body.get('category', None)
                difficulty = body.get('difficulty', None)
                print(answer)
                if ((question) == ""):
                    abort(422)

                new_question = Question(
                    question=question, answer=answer, category=category, difficulty=difficulty)
                new_question.insert()

            return jsonify({
                'success': True,
                'question': new_question.question,
                'answer': new_question.answer,
                'difficulty': new_question.difficulty,
                'category': new_question.category
            })

        except:
            abort(422)

    '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''

    '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''

    @app.route('/categories/<int:type_id>/questions')
    def get_questionsbycategory(type_id):
        current_categoryquestions = Question.query.filter(
            Question.category == type_id).all()

        # get all questions and paginate
        current_questions = paginate_questions(
            request, current_categoryquestions)
        current_category = Category.query.filter(
            Category.id == type_id).one_or_none()
        if (current_category) is None:
            abort(404)

           # abort 404 if no questions
        if len(current_questions) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'questions': current_questions,
            'total_questions': len(current_questions),
            'current_category': {"id": current_category.id, "type": current_category.type}
        })

    '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

    @app.route('/quizzes', methods=['POST'])
    def play_quizz():

        try:

            body = request.get_json()
            previous_questions = body.get('previous_questions', None)
            quiz_category = body.get('quiz_category', None)

            if ((quiz_category is None) or (previous_questions is None)):
                abort(400)

            questions = []
            if quiz_category["id"] == 0:
                questions = Question.query.filter(
                    Question.id.notin_(previous_questions)).all()

            else:
                questions = Question.query.filter(Question.category == quiz_category["id"]).filter(
                    Question.id.notin_(previous_questions)).all()

            random_question = None
            if len(questions) != 0:
                random_question = random.choice(questions).format()

            return jsonify({
                'success': True,
                'question': random_question
            })

        except:
            abort(500)

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 404

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 404

    @app.errorhandler(500)
    def something_wentwrong(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "Something went wrong"
        }), 500

    return app
