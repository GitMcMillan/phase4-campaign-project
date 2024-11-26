#!/usr/bin/env python3

# Standard library imports
from random import randint, sample, choice as rc

# Remote library imports
from faker import Faker

# Local imports
from app import app
from models import db, Character, GameMaster, Player, Session, session_players

if __name__ == '__main__':
    fake = Faker()
    with app.app_context():
        print("Starting seed...")
        # Seed code goes here!

        # clear data
        db.session.query(Player).delete()
        db.session.query(GameMaster).delete()
        db.session.query(Character).delete()
        db.session.query(Session).delete()
        db.session.commit()

        # empty list
        all_characters = []
        all_gamemasters = []
        all_players = []

        # character classes
        classes = ['Fighter', 'Rogue', 'Wizard', 'Bard', 'Paladin', 'Cleric', 'Druid', 'Ranger', 'Monk', 'Barbarian']

        # fantasy character names
        character_names = [
            "Eryndor Shadowbane", "Kaelith Duskwhisper", "Thalric Ironhart",
            "Lirael Moonsong", "Aldor Farsight", "Sylvara Windrider",
            "Dainar Fireforge", "Morrigan Nightshade", "Veylin Frostclaw",
            "Serenna Starfall", "Draven Stormborn", "Isolde Emberstone",
            "Kaelen Darkblade", "Talia Swiftthorn", "Zorath Blackfyre",
            "Elysia Silverbrook", "Rendrick Stormbreaker", "Anara Flameheart",
            "Fenric Wolfsbane", "Thyra Sunveil"
        ]

        # seed characters
        characters = [
            Character(
                name=character_names.pop(character_names.index(rc(character_names))),
                character_class=rc(classes),
                level=randint(1, 5)
            )
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

        # seed sessions
        sessions = [
            Session(name=f"Session {i + 1}", date=fake.date_time_this_year())
            for i in range(5)
        ]
        db.session.add_all(sessions)
        db.session.commit()


        for session in sessions:
            session_players_list = sample(players, randint(2, 5))  # Add 2 to 5 players to each session
            for player in session_players_list:
                is_in_session = rc([True, False])  # Randomly set whether the player is in session
                db.session.execute(
                    session_players.insert().values(
                        session_id=session.id,
                        player_id=player.id,
                        is_in_session=is_in_session
                    )
                )
        db.session.commit()

        print("Seeded!")
