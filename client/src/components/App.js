import React, { useEffect, useState } from "react";
import { Route } from "react-router-dom";
import NavBar from "./NavBar";
import { BrowserRouter as Router, Routes } from "react-router-dom";
import SessionsPage from "./SessionsPage";
import CharactersPage from "./CharactersPage";
import GameMastersPage from "./GameMasters";
import PlayersPage from "./PlayersPage";

function App() {
  const [players, setPlayers] = useState([]);
  const [characters, setCharacters] = useState([]);
  const [gamemasters, setGameMasters] = useState([]);
  const [sessions, setSessions] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/players")
      .then((r) => r.json())
      .then((player_data) => setPlayers(player_data));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/characters")
      .then((r) => r.json())
      .then((characterData) => setCharacters(characterData));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/gamemasters")
      .then((r) => r.json())
      .then((gameMasterData) => setGameMasters(gameMasterData));
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/sessions")
      .then((response) => response.json())
      .then((data) => setSessions(data));
  }, []);

  function HomePage() {
    return <h1>Welcome to the Home Page</h1>;
  }

  return (
    <Router>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route
          path="/players"
          element={<PlayersPage players={players} setPlayers={setPlayers} />}
        />
        <Route
          path="/characters"
          element={
            <CharactersPage
              characters={characters}
              setCharacters={setCharacters}
            />
          }
        />
        <Route
          path="/gamemasters"
          element={
            <GameMastersPage
              gamemasters={gamemasters}
              setGameMasters={setGameMasters}
            />
          }
        />
        <Route
          path="/sessions"
          element={
            <SessionsPage sessions={sessions} setSessions={setSessions} />
          }
        />
      </Routes>
    </Router>
  );
}

export default App;
