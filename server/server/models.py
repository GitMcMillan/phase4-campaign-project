from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.ext.associationproxy import association_proxy

from config import db

# Models go here!

class Character(db.Model, SerializerMixin):
  __tablename__ = 'characters'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  level = db.Column(db.Integer)
  character_class = db.Column(db.String)

  #relationships
  players = db.relationship('Player', back_populates='character')

  #serializer rules
  serialize_rules = ('-players',)

  #repr
  def __repr__(self):
    return f'<Character id={self.id}, name={self.name}, level={self.level}, class={self.character_class}>'

class GameMaster(db.Model, SerializerMixin):
  __tablename__ = 'gamemasters'

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String)
  

  #relationships
  players = db.relationship('Player', back_populates='game_master')

  #serializer rules
  serialize_rules = ('-players',)

  #repr
  def __repr__(self):
    return f'<GameMaster id={self.id}, name={self.name}>'

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

  #serializer
  serialize_rules = ('-game_master', "-character")

  #repr
  def __repr__(self):
    return f'<Player id={self.id}, name={self.name}>'
