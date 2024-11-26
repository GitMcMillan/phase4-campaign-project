#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, jsonify, make_response, request
from flask_restful import Resource

# Local imports
from config import app, db, api
# Add your model imports
from models import Character, GameMaster, Player, Session, session_players
from flask_cors import CORS
from datetime import datetime



CORS(app)




# Views go here!

@app.route('/')
def index():
    return '<h1>Project Server</h1>'


class Players(Resource):
    def get(self):
        players = Player.query.all()
        player_data = [player.to_dict() for player in players]

        if not players:
            return {"message": "players do not exist"}, 404
        
        return player_data, 200
        
    def post(self):
        data = request.get_json()

        if not data.get("name"):
            return jsonify({"error": "Player is required"}), 400

        new_player = Player(
            name=data["name"]
        )

        db.session.add(new_player)
        db.session.commit()

        return new_player.to_dict(), 201
        


class PlayersByID(Resource):
    def get(self, id):
        player = Player.query.filter_by(id=id).first()
        if not player:
            return {"error": "Player does not exist"}, 404
        
        return player.to_dict(), 200
    
    def patch(self, id):
        player = Player.query.filter_by(id=id).first()
        data = request.get_json()
        
        if 'name' in data:
            player.name=data['name']
        
        
        db.session.commit()
        return player.to_dict(), 200
    
    def delete(self, id):
         player = Player.query.filter_by(id=id).first()

         db.session.delete(player)
         db.session.commit()

         return "", 204 


class Characters(Resource):
    def get(self):
        characters = Character.query.all()
        characters_data = [character.to_dict() for character in characters]

        if not characters:
            return make_response({"error": "Characters does not exist"}, 404)
        
        return make_response(characters_data, 200)
    
    def post(self):
        data = request.get_json()

        new_character = Character(
            name=data["name"],
            level=data["level"],
            character_class=data["character_class"]
        )
        db.session.add(new_character)
        db.session.commit()

        return make_response(new_character.to_dict(), 201)


class CharactersByID(Resource):
    def get(self, id):
        character = Character.query.filter_by(id=id).first()

        if not character:
            return make_response({"error": "Character does not exist"})
        return make_response(character.to_dict(), 201)
    
    def patch(self, id):
        character = Character.query.filter_by(id=id).first()
        data = request.get_json()
        
        if 'name' in data:
            character.name=data['name']
        if 'level' not in data:
            character.level=data['level']
        if 'character_class' not in data:
            character.character_class=data['character_class']
        
        
        db.session.commit()
        return make_response(character.to_dict(), 200)
    
    def delete(self, id):
         character = Character.query.filter_by(id=id).first()

         db.session.delete(character)
         db.session.commit()

         return "", 204 
    
class Characters_by_level(Resource):
    def get(self):
        characters = Character.query.filter(Character.level > 2).all()

        character_levels = [character.to_dict() for character in characters]

        return make_response(character_levels, 200)

api.add_resource(Characters_by_level, '/charactersbylevel')

class GameMasters(Resource):
    def get(self):
        game_masters = GameMaster.query.all()
        game_master_data = [game_master.to_dict() for game_master in game_masters]

        if not game_masters:
            return make_response({"message": "game_masters do not exist"}, 404)
        
        return make_response(game_master_data, 200)
        
    def post(self):
        data = request.get_json()

        if not data.get("name"):
            return make_response({"error": "gamemaster is required"}, 400)

        new_game_master = GameMaster(
            name=data["name"]
        )

        db.session.add(new_game_master)
        db.session.commit()

        return make_response(new_game_master.to_dict(), 201)
    

class GameMastersByID(Resource):
    def get(self, id):
        game_master = GameMaster.query.filter_by(id=id).first()

        if not game_master:
            return make_response({"error": "game_master does not exist"})
        return make_response(game_master.to_dict(), 201)
    
    def patch(self, id):
        game_master = GameMaster.query.filter_by(id=id).first()
        data = request.get_json()
        
        if 'name' in data:
            game_master.name=data['name']
        
        
        
        db.session.commit()
        return make_response(game_master.to_dict(), 200)
    
    def delete(self, id):
         game_master = GameMaster.query.filter_by(id=id).first()

         db.session.delete(game_master)
         db.session.commit()

         return "", 204


class Sessions(Resource):
    def get(self):
        sessions = Session.query.all()
        return [session.to_dict() for session in sessions], 200

    def post(self):
        data = request.get_json()
        if not data.get('name') or not data.get('date'):
            return make_response({"error": "Name and date are required"}, 400)

        try:
            date = datetime.strptime(data['date'], "%Y-%m-%d")
        except ValueError:
            return make_response({"error": "Invalid date format. Use YYYY-MM-DD."}, 400)

        new_session = Session(
            name=data['name'],
            date=date
        )
        db.session.add(new_session)
        db.session.commit()
        return make_response(new_session.to_dict(), 201)


class SessionByID(Resource):
    def get(self, id):
        session = Session.query.filter_by(id=id).first()
        if not session:
            return {"error": "Session not found"}, 404
        return make_response(session.to_dict(), 200)

    def patch(self, id):
        session = Session.query.filter_by(id=id).first()
        if not session:
            return make_response({"error": "Session not found"}, 404)

        data = request.get_json()
        if 'name' in data:
            session.name = data['name']
        if 'date' in data:
            try:
                session.date = datetime.strptime(data['date'], "%Y-%m-%d")
            except ValueError:
                return make_response({"error": "Invalid date format. Use YYYY-MM-DD."}, 400)

        db.session.commit()
        return session.to_dict(), 200

    def delete(self, id):
        session = Session.query.filter_by(id=id).first()
        if not session:
            return make_response({"error": "Session not found"}, 404)

        db.session.delete(session)
        db.session.commit()
        return "", 204


class SessionPlayerStatus(Resource):
    def patch(self, session_id, player_id):
        data = request.get_json()
        is_in_session = data.get('is_in_session')

        if is_in_session is None:
            return make_response({"error": "is_in_session is required"}, 400)

        stmt = session_players.update().where(
            (session_players.c.session_id == session_id) &
            (session_players.c.player_id == player_id)
        ).values(is_in_session=is_in_session)

        db.session.execute(stmt)
        db.session.commit()

        return make_response({
            "session_id": session_id,
            "player_id": player_id,
            "is_in_session": is_in_session
        }, 200)




api.add_resource(Players, '/players')
api.add_resource(PlayersByID, '/players/<int:id>')
api.add_resource(Characters, '/characters')
api.add_resource(CharactersByID, '/characters/<int:id>')
api.add_resource(GameMasters, '/gamemasters')
api.add_resource(GameMastersByID, '/gamemasters/<int:id>')
api.add_resource(Sessions, '/sessions')
api.add_resource(SessionByID, '/sessions/<int:id>')
api.add_resource(SessionPlayerStatus, '/sessions/<int:session_id>/players/<int:player_id>')


# @app.route('/players', methods= ["GET", "POST"])
# def get_players():
#     if request.method == "GET":
#         players = Player.query.all()
#         player_data = [player.to_dict() for player in players]

#         return jsonify(player_data)

#     elif request.method == "POST":
    
#         data = request.get_json()

#         if not data.get("name"):
#             return jsonify({"error": "Player is required"}), 400

#         new_player = Player(
#             name=data["name"]
#         )

#         db.session.add(new_player)
#         db.session.commit()

#         return jsonify(new_player.to_dict()), 201    

# @app.route('/players/<int:id>', methods= ["GET", "PATCH", "DELETE"])
# def player_by_id(id):
#     player = Player.query.filter_by(id=id).first()

#     if not player:
#             return make_response(jsonify({"error": "Player not found"}), 404)

#     if request.method == "GET":
#         return jsonify(player.to_dict()), 200
    
#     elif request.method == "PATCH":
#         data = request.get_json()
        
#         if 'name' in data:
#             player.name=data['name']
        
        
#         db.session.commit()
#         return jsonify(player.to_dict()), 200
    
#     elif request.method == "DELETE":

#         db.session.delete(player)
#         db.session.commit()

#         return "", 204



# @app.route('/characters', methods=['GET','POST'])
# def characters():
#     if request.method == 'POST':
#         data = request.get_json()
#         new_character = Character(
#             name=data['name'],
#             level=data['level'],
#             character_class=data['character_class']
#         )
#         db.session.add(new_character)
#         db.session.commit()
#         return jsonify(new_character.to_dict())
    

    
#     elif request.method == 'GET':
#         characters = Character.query.all()
#         return jsonify([character.to_dict() for character in characters])
    
# @app.route('/characters/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
# def update_characters(id):
#     character = Character.query.filter_by(id=id).first()
#     # print(f"Character found: {character}")  

#     if not character:
#         return jsonify({"error": "Character not found"}), 404
    
#     if request.method=='GET':
#         return jsonify(character.to_dict()), 200


#     if request.method == 'PATCH':
#         data = request.get_json()

#         if 'name' in data:
#             character.name=data['name']
#         if 'level' in data:
#             character.level=data['level']
#         if 'character_class' in data:
#             character.character_class=data['character_class']
        
#         db.session.commit()
#         return jsonify(character.to_dict()), 200
    
#     elif request.method == 'DELETE':
#         db.session.delete(character)
#         db.session.commit()
#         return '', 204


# @app.route('/gamemasters', methods=['GET', 'POST'])
# def gamemasters():
    

#     if request.method == 'POST':
#         data = request.get_json()
#         new_gamemaster = GameMaster(
#             name=data['name'],
#             )
#         db.session.add(new_gamemaster)
#         db.session.commit()
#         return jsonify(new_gamemaster.to_dict())
#     elif request.method == 'GET':
#         game_masters = GameMaster.query.all()
#         return jsonify([game_master.to_dict(rules=("-characters", '-players.sessions')) for game_master in game_masters])
    

# @app.route('/gamemasters/<int:id>', methods=['GET', 'PATCH', "DELETE"])
# def update_gamemaster(id):
#     #grab the instance by id
#     gamemaster = GameMaster.query.filter_by(id=id).first()
#     #data variable for get_json
#     data = request.get_json 

#     #check if it exists
#     if not gamemaster:
#         return jsonify({"error": "Gamemaster not found"}), 404

#     #if/else for patch/delete/get
#     elif request.method == "GET":
#         return jsonify(gamemaster.to_dict()), 200

#     elif request.method == "PATCH":
#         #for patch request json for attributes for new_gamemaster
#         if "name" in data:
#             gamemaster.name=gamemaster['name']
#         db.session.commit()
        
#         return jsonify(gamemaster.to_dict()), 200
    
#     elif request.method == "DELETE":
#         db.session.delete(gamemaster)
#         db.session.commit()
#         return '', 204
    
    


# @app.route('/sessions', methods=['GET', 'POST'])
# def handle_sessions():
#     if request.method == 'POST':
#         data = request.get_json()
#         if not data.get('name') or not data.get('date'):
#             return jsonify({'error': 'Name and date are required'}), 400
        
#         try:
#             date = datetime.strptime(data['date'], "%Y-%m-%d")  # Convert date string to datetime object
#         except ValueError:
#             return jsonify({'error': 'Invalid date format. Use YYYY-MM-DD.'}), 400

        
#         new_session = Session(
#             name=data['name'],
#             date=date
#         )
#         db.session.add(new_session)
#         db.session.commit()
#         return jsonify(new_session.to_dict()), 201

#     elif request.method == 'GET':
#         sessions = Session.query.all()
#         return jsonify([session.to_dict() for session in sessions]), 200
    

# @app.route('/sessions/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
# def handle_session(id):
#     session = Session.query.filter_by(id=id).first()
#     if not session:
#         return jsonify({'error': 'Session not found'}), 404

#     if request.method == 'GET':
#         return jsonify(session.to_dict()), 200

#     elif request.method == 'PATCH':
#         data = request.get_json()
#         if 'name' in data:
#             session.name = data['name']
#         if 'date' in data:
#             session.date = data['date']
#         db.session.commit()
#         return jsonify(session.to_dict()), 200

#     elif request.method == 'DELETE':
#         db.session.delete(session)
#         db.session.commit()
#         return '', 204
    
# @app.route('/sessions/<int:session_id>/players/<int:player_id>', methods=['PATCH'])
# def update_session_player_status(session_id, player_id):
#     data = request.get_json()
#     is_in_session = data.get('is_in_session')

#     if is_in_session is None:
#         return jsonify({"error": "is_in_session is required"}), 400

#     stmt = session_players.update().where(
#         (session_players.c.session_id == session_id) &
#         (session_players.c.player_id == player_id)
#     ).values(is_in_session=is_in_session)

#     db.session.execute(stmt)
#     db.session.commit()

#     return jsonify({
#         "session_id": session_id,
#         "player_id": player_id,
#         "is_in_session": is_in_session
#     }), 200
    


if __name__ == '__main__':
    app.run(port=5555, debug=True)

