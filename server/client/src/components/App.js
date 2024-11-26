import React, { useEffect, useState } from "react";
import { Switch, Route } from "react-router-dom";
import NavBar from "./NavBar";
import { BrowserRouter as Router, Routes } from "react-router-dom";

function App() {
  const [players, setPlayers] = useState([]);
  const [characters, setCharacters] = useState([]);
  const [gamemasters, setGameMasters] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/players")
      .then((r) => r.json())
      .then((player_data) => setPlayers(player_data));
  }, []);
  console.log(players);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/characters")
      .then((r) => r.json())
      .then((characterData) => setCharacters(characterData));
  }, []);
  console.log(characters);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/gamemasters")
      .then((r) => r.json())
      .then((gameMasterData) => setGameMasters(gameMasterData));
  }, []);
  console.log(gamemasters);

  function HomePage() {
    return <h1>Welcome to the Home Page</h1>;
  }

  function PlayersPage({ players }) {
    return (
      <div>
        <h1>Player Info</h1>
        <ul>
          {players.map((player) => (
            <li key={player.id}>Player: {player.name} </li>
          ))}
        </ul>
      </div>
    );
  }

  function CharactersPage({ characters }) {
    return (
      <div>
        <h1>Character Info</h1>
        <ul>
          {characters.map((character) => (
            <li key={character.id}>
              {character.name} - Level {character.level} (
              {character.character_class})
            </li>
          ))}
        </ul>
      </div>
    );
  }

  function GameMastersPage({ gamemasters }) {
    return (
      <div>
        <h1>Game Master Info</h1>
        <ul>
          {gamemasters.map((gamemaster) => (
            <li key={gamemaster.id}>GameMaster: {gamemaster.name}</li>
          ))}
        </ul>
      </div>
    );
  }

  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/players" element={<PlayersPage players={players} />} />
        <Route
          path="/characters"
          element={<CharactersPage characters={characters} />}
        />
        <Route
          path="/gamemasters"
          element={<GameMastersPage gamemasters={gamemasters} />}
        />
      </Routes>
    </Router>
  );
}

export default App;
