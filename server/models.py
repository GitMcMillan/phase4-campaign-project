from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.orm import validates
from datetime import datetime

from config import db

# Models go here!

class Character(db.Model, SerializerMixin):
  __tablename__ = 'characters'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  level = db.Column(db.Integer)
  character_class = db.Column(db.String)

  #relationships
  players = db.relationship('Player', back_populates='character')

  #serializer rules
  serialize_rules = ('-players.character',)

  @validates("name" , "character_class")
  def validation_name_class(self, key, value):
    if not value:
      raise ValueError(f"{key} must be provided and cannot be empty.")
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string.")
    return value
  
  @validates("level")
  def validation_level(self, key, value):
    if not value:
      raise ValueError(f"{key} must be provided and cannot be empty.")
    if not isinstance(value, int):
        raise ValueError(f"{key} must be an integer.")
    return value

  

  #repr
  def __repr__(self):
    return f'<Character id={self.id}, name={self.name}, level={self.level}, class={self.character_class}>'

class GameMaster(db.Model, SerializerMixin):
  __tablename__ = 'gamemasters'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String, nullable=False)
  
  #relationships
  players = db.relationship('Player', back_populates='game_master')

  #serializer rules
  serialize_rules = ('-players.game_master', '-players.character')

  #validation
  @validates("name")
  def validation_name(self, key, value):
    if not value:
      raise ValueError(f"{key} must be provided and cannot be empty.")
    return value

  #repr
  def __repr__(self):
    return f'<GameMaster id={self.id}, name={self.name}>'
  

class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    role = db.Column(db.String, nullable=False) 

    # Many-to-Many w/player
    players = db.relationship('Player', secondary='session_players', back_populates='sessions')

    serialize_rules = ('-players.sessions', '-players.character')

    #validation
    @validates("name", "role")
    def validation_name_role(self, key, value):
      if not value:
        raise ValueError(f"{key} must be provided and cannot be empty.")
      return value
    
    @validates("date")
    def validate_date(self, key, value):
      if not isinstance(value, datetime):
          raise ValueError(f"{key} must be a valid datetime object.")
      return value


session_players = db.Table(
    'session_players',
    db.Column('session_id', db.Integer, db.ForeignKey('sessions.id'), primary_key=True),
    db.Column('player_id', db.Integer, db.ForeignKey('players.id'), primary_key=True),
    db.Column('is_in_session', db.Boolean, default=True)
)



class Player(db.Model, SerializerMixin):
  __tablename__ = 'players'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  # gamemaster_id = db.Column(db.Integer, db.ForeignKey('gamemasters.id'))
  # character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

  #relationships/foreign keys
  gamemaster_id = db.Column(db.Integer, db.ForeignKey('gamemasters.id'))

  character_id = db.Column(db.Integer, db.ForeignKey('characters.id'))

  game_master = db.relationship('GameMaster', back_populates="players")
  
  character = db.relationship('Character', back_populates='players')

  sessions = db.relationship('Session', secondary='session_players', back_populates='players')

  #serializer
  serialize_rules = ('-game_master.players', "-character.players", '-sessions.players')

  @validates("name")
  def validation(self, key, value):
    if not value:
      raise ValueError(f"{key} must be provided and cannot be empty.")
    if not isinstance(value, str):
        raise ValueError(f"{key} must be a string.")
    return value

  

  #repr
  def __repr__(self):
    return f'<Player id={self.id}, name={self.name}>'
