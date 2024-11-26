# Welcome to my DnD Session Tracker App

For those unfamiliar with the game Dungeons and Dragons (or any tabletop RPG game), the essentials are:

1. Every player has one character that they play at one session.
2. Every session has one GameMaster to guide the players, game, and story.
3. Every session would have one GameMaster and many players, each with one character.

So:
- Every player has one character and one GameMaster for one Session.
- Every GameMaster has many players and one session.
- Every session has one GameMaster and many players.

---

## TABLETOP GAME MANAGER

This project provides a RESTful API for managing these games, the characters they play, and the sessions and GameMasters they will play with. The API allows CRUD operations for all tables while maintaining relationships between GameMasters and characters used by the players within each session.

---

## Technologies Used

- Python 3.8.13
- Flask: A lightweight WSGI web application framework
- Flask-SQLAlchemy: A SQL toolkit for Python
- Flask-RESTful: An extension for Flask that adds support for quickly building REST APIs
- Flask-Migrate: A SQLAlchemy database migration framework
- Flask-CORS: A Flask extension for handling Cross-Origin Resource Sharing (CORS)
- SQLAlchemy: SQL toolkit and Object-Relational Mapping (ORM)
- Faker: A library for generating fake data
- Alembic: A lightweight database migration tool for SQLAlchemy
- React: A JavaScript library for building user interfaces

---

## Project Setup

### Installation

Clone this repository:

```bash
git clone <repository-url>
cd <repository-name>
```

Create a virtual environment and activate it:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### Initialize the Database and Run Migrations

```bash
flask db upgrade
```

To seed the database with sample data, run:

```bash
python seed.py
```

---

## Running the Server

To start the server, run the following command:

```bash
python app.py
```

By default, the server will be hosted on [http://localhost:5555](http://localhost:5555).

---

## Running the Client

Navigate to the client directory and install the dependencies:

```bash
cd client
npm install
```

Start the client application:

```bash
npm start
```

By default, the client will be hosted on [http://localhost:3000](http://localhost:3000).

---

## Database Seeding

To populate the database with sample data, run the seeding script:

```bash
python seed.py
```

---

## Migrations

This project uses Alembic for database migrations.

To generate a new migration:

```bash
flask db migrate -m "Migration message"
```

To apply the migration:

```bash
flask db upgrade

