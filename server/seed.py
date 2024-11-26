#!/usr/bin/env python3

# Standard library imports
from random import randint, choice as rc
import random

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Character, GameMaster, Player, Session

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        #clear data
        db.session.query(Player).delete()
        db.session.query(GameMaster).delete()
        db.session.query(Character).delete()
        db.session.query(Session).delete()
        db.session.commit()


        #add instances test

        #empty list
        all_characters = []
        all_gamemasters = []
        all_players = []

        #character classes
        classes = ['Fighter', 'Rogue', 'Wizard', 'Bard', 'Paladin', 'Cleric', 'Druid', 'Ranger', 'Monk', 'Barbarian', 'Warlock']

        character_names = ["Eryndor Shadowbane",
        "Kaelith Duskwhisper",
        "Thalric Ironhart",
        "Lirael Moonsong",
        "Aldor Farsight",
        "Sylvara Windrider",
        "Dainar Fireforge",
        "Morrigan Nightshade",
        "Veylin Frostclaw",
        "Serenna Starfall",
        "Draven Stormborn",
        "Isolde Emberstone",
        "Kaelen Darkblade",
        "Talia Swiftthorn",
        "Zorath Blackfyre",
        "Elysia Silverbrook",
        "Rendrick Stormbreaker",
        "Anara Flameheart",
        "Fenric Wolfsbane",
        "Thyra Sunveil"]

        
        
        # seed characters 
        characters = [
            Character(name=character_names.pop(character_names.index(rc(character_names))), character_class=rc(classes), level=randint(1, 5))
            for _ in range(10)
        ]
        db.session.add_all(characters)
        db.session.commit()  

        # seed GameMasters 
        gamemasters = [GameMaster(name=fake.first_name()) for _ in range(5)]
        db.session.add_all(gamemasters)
        db.session.commit()  

        # seed Players 
        all_characters = Character.query.all()
        all_gamemasters = GameMaster.query.all()
        
        players = [
            Player(
                name=fake.first_name(),
                gamemaster_id=rc(all_gamemasters).id,
                character_id=rc(all_characters).id
            )
            for _ in range(10)
        ]
        db.session.add_all(players)
        db.session.commit()  
        

        # sessions
        print("Seeding sessions...")
        sessions = [
            Session(name=f"Session {i + 1}", date=fake.date_time_this_year(),  role="Player Character")
            for i in range(5)
        ]
        db.session.add_all(sessions)
        db.session.commit()

         # players with Sessions
        print("Associating players with sessions...")
        all_sessions = Session.query.all()
        for session in all_sessions:
            session_players = random.sample(players, randint(2, min(5, len(players))))  # Add 2-5 random players to session
            session.players.extend(session_players)
        db.session.commit()

        # breakpoint()

        print("Seeded!")

            

      
