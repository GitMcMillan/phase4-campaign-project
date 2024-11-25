import React, { useState, useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

function SessionsPage({ sessions, setSessions }) {
  const [players, setPlayers] = useState([]);
  const [selectedSession, setSelectedSession] = useState(null);
  const [sessionPlayers, setSessionPlayers] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/players")
      .then((response) => response.json())
      .then((data) => setPlayers(data));
  }, []);

  const fetchSessionPlayers = (sessionId) => {
    fetch(`http://127.0.0.1:5555/sessions/${sessionId}`)
      .then((response) => response.json())
      .then((sessionData) => setSessionPlayers(sessionData.players || []));
  };

  const togglePlayerStatus = (sessionId, playerId, currentStatus) => {
    fetch(`http://127.0.0.1:5555/sessions/${sessionId}/players/${playerId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ is_in_session: !currentStatus }),
    })
      .then((response) => response.json())
      .then(() => {
        setSessionPlayers((prevPlayers) =>
          prevPlayers.map((player) =>
            player.id === playerId
              ? { ...player, is_in_session: !currentStatus }
              : player
          )
        );
      })
      .catch((error) => console.error("Error:", error));
  };

  const addPlayerSchema = Yup.object().shape({
    player_id: Yup.string().required("Player is required"),
    notes: Yup.string().optional(),
  });

  return (
    <div>
      <h1>Sessions</h1>
      <ul>
        {sessions.map((session) => (
          <li key={session.id}>
            {session.name} - {new Date(session.date).toLocaleDateString()}
            <button
              onClick={() => {
                setSelectedSession(session.id);
                fetchSessionPlayers(session.id);
              }}
            >
              View/Add Players
            </button>
          </li>
        ))}
      </ul>

      {selectedSession && (
        <div>
          <h2>Session Players</h2>
          <ul>
            {sessionPlayers.map((player) => (
              <li key={player.id}>
                {player.name} - Notes: {player.notes || "No notes"} -{" "}
                <strong>
                  {player.is_in_session ? "In Session" : "Out of Session"}
                </strong>
                <button
                  onClick={() =>
                    togglePlayerStatus(
                      selectedSession,
                      player.id,
                      player.is_in_session
                    )
                  }
                >
                  Toggle Status
                </button>
              </li>
            ))}
          </ul>

          <h2>Add Player to Session</h2>
          <Formik
            initialValues={{ player_id: "", notes: "" }}
            validationSchema={addPlayerSchema}
            onSubmit={(values, { resetForm }) => {
              fetch(
                `http://127.0.0.1:5555/sessions/${selectedSession}/players`,
                {
                  method: "POST",
                  headers: { "Content-Type": "application/json" },
                  body: JSON.stringify(values),
                }
              )
                .then((response) => response.json())
                .then(() => {
                  resetForm();
                  fetchSessionPlayers(selectedSession);
                })
                .catch((error) => console.error("Error:", error));
            }}
          >
            {() => (
              <Form>
                <div>
                  <label>Player:</label>
                  <Field as="select" name="player_id">
                    <option value="">Select a Player</option>
                    {players.map((player) => (
                      <option key={player.id} value={player.id}>
                        {player.name}
                      </option>
                    ))}
                  </Field>
                  <ErrorMessage name="player_id" component="div" />
                </div>
                <div>
                  <label>Notes:</label>
                  <Field as="textarea" name="notes" placeholder="Enter notes" />
                  <ErrorMessage name="notes" component="div" />
                </div>
                <button type="submit">Add Player</button>
              </Form>
            )}
          </Formik>
        </div>
      )}
    </div>
  );
}

export default SessionsPage;
