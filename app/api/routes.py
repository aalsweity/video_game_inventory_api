from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Game, game_schema, games_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'game name': 'super mario bros.',
            'game genre': 'side scroller',
            'game rating' : 'E',
            'game grade' : 'Awesome'
            }
    
@api.route('/inventory', methods = ['POST'])
@token_required
def create_game(current_user_token):
    game_name = request.json['game_name']
    game_genre = request.json['game_genre']
    game_rating = request.json['game_rating']
    game_grade = request.json['game_grade']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    game = Game(game_name, game_genre, game_rating, game_grade, user_token = user_token )

    db.session.add(game)
    db.session.commit()

    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/inventory', methods = ['GET'])
@token_required
def get_game(current_user_token):
    a_user = current_user_token.token
    games = Game.query.filter_by(user_token = a_user).all()
    response = games_schema.dump(games)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['GET'])
@token_required
def get_single_game(current_user_token, id):
    game = Game.query.get(id)
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['POST','PUT'])
@token_required
def update_game(current_user_token,id):
    game = Game.query.get(id) 
    game.game_name = request.json['game_name']
    game.game_genre = request.json['game_genre']
    game.game_rating = request.json['game_rating']
    game.game_grade = request.json['game_grade']
    game.user_token = current_user_token.token

    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)

@api.route('/inventory/<id>', methods = ['DELETE'])
@token_required
def delete_game(current_user_token, id):
    game = Game.query.get(id)
    db.session.delete(game)
    db.session.commit()
    response = game_schema.dump(game)
    return jsonify(response)