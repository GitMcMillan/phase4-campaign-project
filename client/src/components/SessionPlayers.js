import React, { useState, useEffect } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

const SessionPlayers = ({ sessionId }) => {
  const [players, setPlayers] = useState([]);

  useEffect(() => {
    fetch(`/sessions/${sessionId}/players`)
      .then((response) => response.json())
      .then((data) => setPlayers(data));
  }, [sessionId]);

  const toggleStatus = (playerId, currentStatus) => {
    fetch(`/sessions/${sessionId}/players/${playerId}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ is_in_session: !currentStatus }),
    })
      .then((response) => response.json())
      .then((updatedPlayer) => {
        setPlayers((prevPlayers) =>
          prevPlayers.map((player) =>
            player.id === updatedPlayer.id ? updatedPlayer : player
          )
        );
      });
  };

  const addPlayerSchema = Yup.object().shape({
    player_id: Yup.string().required("Player is required"),
    notes: Yup.string().optional(),
  });

  return (
    <div>
      <h2>Session Players</h2>
      <ul>
        {players.map((player) => (
          <li key={player.id}>
            {player.name} -{" "}
            <strong>
              {player.is_in_session ? "In Session" : "Out of Session"}
            </strong>
            <button
              onClick={() => toggleStatus(player.id, player.is_in_session)}
            >
              Toggle
            </button>
          </li>
        ))}
      </ul>

      <h3>Add a Player to the Session</h3>
      <Formik
        initialValues={{ player_id: "", notes: "" }}
        validationSchema={addPlayerSchema}
        onSubmit={(values, { resetForm }) => {
          fetch(`/sessions/${sessionId}/players`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(values),
          })
            .then((response) => response.json())
            .then((newPlayer) => {
              setPlayers((prevPlayers) => [...prevPlayers, newPlayer]);
              resetForm();
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
                {/* Dynamically populate players for the dropdown if required */}
              </Field>
              <ErrorMessage name="player_id" component="div" />
            </div>
            <div>
              <label>Notes:</label>
              <Field
                as="textarea"
                name="notes"
                placeholder="Enter notes here"
              />
              <ErrorMessage name="notes" component="div" />
            </div>
            <button type="submit">Add Player</button>
          </Form>
        )}
      </Formik>
    </div>
  );
};

export default SessionPlayers;
