import os
from flask import Flask, request, jsonify, abort
from flask import make_response
from sqlalchemy import exc
import json
from flask_cors import CORS

from .database.models import db_drop_and_create_all, setup_db, Drink
from .auth.auth import AuthError, requires_auth

app = Flask(__name__)
setup_db(app)
CORS(app)

'''
@DONE uncomment the following line to initialize the datbase
!! NOTE THIS WILL DROP ALL RECORDS AND START YOUR DB FROM SCRATCH
!! NOTE THIS MUST BE UNCOMMENTED ON FIRST RUN
'''
db_drop_and_create_all()

# ROUTES
'''
@DONE implement endpoint
    GET /drinks
        it should be a public endpoint
        it should contain only the drink.short() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks', methods=['GET'])
def get_drinks():
    '''
    public end point
    fetches all drinks and applies short description
    '''
    try:
        return make_response(jsonify({
            'success': True,
            'drinks': [drink.short() for drink in Drink.query.all()]
        }), 200)
    except BaseException:
        return make_response(jsonify({
            'success': False,
            'error': 'Couldnt GET drinks'
        }), 500)


'''
@DONE implement endpoint
    GET /drinks-detail
        it should require the 'get:drinks-detail' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drinks} where drinks is the list of drinks
        or appropriate status code indicating reason for failure
'''

# since it requires auth we need to pass in function.


@app.route('/drinks-detail', methods=['GET'])
@requires_auth('get:drinks-detail')
def get_drinks_detail(f):
    '''
    API point that requires auth. Returns all drinks with
    long description
    '''
    try:
        return make_response(jsonify({
            'success': True,
            'drinks': [drink.long() for drink in Drink.query.all()]
        }), 200)
    except BaseException:
        return make_response(jsonify({
            'success': False,
            'drinks': 'Couldnt GET drinks (long)'
        }), 500)


'''
@TODO implement endpoint
    POST /drinks
        it should create a new row in the drinks table
        it should require the 'post:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the newly created drink
        or appropriate status code indicating reason for failure
'''

# since it needs auth we pass in function


@app.route('/drinks', methods=['POST'])
@requires_auth('post:drinks')
def post_drinks(f):
    '''
    create new drink and return new drink long description json
    '''
    # get data from post request
    data = dict(request.form or request.json or request.data)
    drink = Drink(
        title=data.get('title'),
        recipe=data.get('recipe') if isinstance(
            data.get('recipe'),
            str) else json.dumps(
            data.get('recipe')))
    try:
        drink.insert()
        return json.dumps({'success': True, 'drink': drink.long()}), 200
    except BaseException:
        return json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500

    return make_response(jsonify({
        'success': True,
        'drinks': [drink.long()]
    }), 200)


'''
@TODO implement endpoint
    PATCH /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should update the corresponding row for <id>
        it should require the 'patch:drinks' permission
        it should contain the drink.long() data representation
    returns status code 200 and json {"success": True, "drinks": drink} where drink an array containing only the updated drink
        or appropriate status code indicating reason for failure
'''

# requires auth, must pass function and id


@app.route('/drinks/<id>', methods=['PATCH'])
@requires_auth('patch:drinks')
def edit_drink(f, id):
    '''
    Update drink if it exists and return drink info
    '''
    try:
        # get data from form request
        req = request.get_json()
        # get drink by id, return none if it doesnt exist
        drink = Drink.query.filter_by(id=id).one_or_none()

        # if it exists
        if drink:
            drink.title = req.get('title') if data.get(
                'title') else drink.title
            recipe = data.get('recipe') if data.get('recipe') else drink.recipe
            drink.recipe = recipe if isinstance(
                recipe, str) else json.dumps(recipe)
            drink.update()
            return make_response(jsonify({
                'success': True,
                'drinks': [drink.long()]
            }), 200)
        else:
            return make_response(jsonify({
                'success': False,
                'error': 'Drink ' + str(id) + ' doesnt exist.'
            }), 404)
    except BaseException:
        return make_response(jsonify({
            'success': False,
            'error': "An error occurred"
        }), 500)


'''
@TODO implement endpoint
    DELETE /drinks/<id>
        where <id> is the existing model id
        it should respond with a 404 error if <id> is not found
        it should delete the corresponding row for <id>
        it should require the 'delete:drinks' permission
    returns status code 200 and json {"success": True, "delete": id} where id is the id of the deleted record
        or appropriate status code indicating reason for failure
'''


@app.route('/drinks/<id>', methods=['DELETE'])
@requires_auth('delete:drinks')
def delete_drink(f, id):
    '''
    deletes drink if it exists
    '''
    try:
        # get drink by id, returns none if it doesnt exist
        drink = Drink.query.filter_by(id=id).one_or_none()

        # delete if it exists
        if drink:
            drink.delete()
            return make_response(jsonify({
                'success': True,
                'drink': id
            }), 200)
        else:
            return make_response(jsonify({
                'success':
                False,
                'error':
                'Drink #' + id + ' not found to be deleted'
            }), 404)
    except BaseException:
        return make_response(json.dumps({
            'success': False,
            'error': "An error occurred"
        }), 500)


# Error Handling
'''
Example error handling for unprocessable entity
'''


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


'''
@DONE implement error handlers using the @app.errorhandler(error) decorator
    each error handler should return (with approprate messages):
             jsonify({
                    "success": False,
                    "error": 404,
                    "message": "resource not found"
                    }), 404

'''


@app.errorhandler(400)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Error in request body."
    }), 400


'''
@DONE implement error handler for 404
    error handler should conform to general task above
'''


@app.errorhandler(404)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


'''
@DONE implement error handler for AuthError
    error handler should conform to general task above
'''


@app.errorhandler(AuthError)
def auth_error_handler(auth_error):
    res = jsonify(auth_error.error)
    res.status_code = auth_error.status_code
    return res
