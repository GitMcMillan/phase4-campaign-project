#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import Character, GameMaster, Player
from flask_cors import CORS


CORS(app)




# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'

@app.route('/players')
def get_players():
    players = Player.query.all()
    player_data = [player.to_dict() for player in players]

    return jsonify(player_data)



@app.route('/characters', methods=['GET','POST'])
def characters():
    if request.method == 'POST':
        data = request.get_json()
        new_character = Character(
            name=data['name'],
            level=data['level'],
            character_class=data['character_class']
        )
        db.session.add(new_character)
        db.session.commit()
        return jsonify(new_character.to_dict())
    elif request.method == 'GET':
        characters = Character.query.all()
        return jsonify([character.to_dict() for character in characters])
    
@app.route('/characters/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def update_characters(id):
    character = Character.query.filter_by(id=id).first()
    # print(f"Character found: {character}")  

    if not character:
        return jsonify({"error": "Character not found"}), 404
    
    if request.method=='GET':
        return jsonify(character.to_dict()), 200


    if request.method == 'PATCH':
        data = request.get_json()

        if 'name' in data:
            character.name=data['name']
        if 'level' in data:
            character.level=data['level']
        if 'character_class' in data:
            character.character_class=data['character_class']
        
        db.session.commit()
        return jsonify(character.to_dict()), 200
    
    elif request.method == 'DELETE':
        db.session.delete(character)
        db.session.commit()
        return '', 204


@app.route('/gamemasters', methods=['GET', 'POST'])
def gamemasters():
    

    if request.method == 'POST':
        data = request.get_json()
        new_gamemaster = GameMaster(
            name=data['name'],
            )
        db.session.add(new_gamemaster)
        db.session.commit()
        return jsonify(new_gamemaster.to_dict())
    elif request.method == 'GET':
        game_masters = GameMaster.query.all()
        return jsonify([game_master.to_dict() for game_master in game_masters])
    

@app.route('/gamemasters/<int:id>', methods=['GET', 'PATCH', "DELETE"])
def update_gamemaster(id):
    #grab the instance by id
    gamemaster = GameMaster.query.filter_by(id=id).first()
    #data variable for get_json
    data = request.get_json 

    #check if it exists
    if not gamemaster:
        return jsonify({"error": "Gamemaster not found"}), 404

    #if/else for patch/delete/get
    elif request.method == "GET":
        return jsonify(gamemaster.to_dict()), 200

    elif request.method == "PATCH":
        #for patch request json for attributes for new_gamemaster
        if "name" in data:
            gamemaster.name=gamemaster['name']
        db.session.commit()
        
        return jsonify(gamemaster.to_dict()), 200
    
    elif request.method == "DELETE":
        db.session.delete(gamemaster)
        db.session.commit()
        return '', 204
    
    


@app.route('/sessions')
def get_sessions():
    return '<h1>Sessions route working</h1>'
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)

