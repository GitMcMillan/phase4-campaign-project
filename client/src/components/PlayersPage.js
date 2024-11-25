import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

function PlayersPage({ players, setPlayers }) {
  const [editingPlayer, setEditingPlayer] = useState(null);

  // validation
  const playerSchema = Yup.object().shape({
    name: Yup.string().required("Player name is required"),
  });

  // post
  const handleAddPlayer = (values, { resetForm }) => {
    fetch("http://127.0.0.1:5555/players", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((newPlayer) => {
        setPlayers((prev) => [...prev, newPlayer]);
        resetForm();
      });
  };

  // patvh
  const handleEditPlayer = (values) => {
    fetch(`http://127.0.0.1:5555/players/${editingPlayer.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((updatedPlayer) => {
        setPlayers((prev) =>
          prev.map((player) =>
            player.id === updatedPlayer.id ? updatedPlayer : player
          )
        );
        setEditingPlayer(null);
      });
  };

  // delete
  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5555/players/${id}`, {
      method: "DELETE",
    }).then(() => {
      setPlayers((prev) => prev.filter((player) => player.id !== id));
    });
  };

  return (
    <div>
      <h1>Players</h1>
      <ul>
        {players.map((player) => (
          <li key={player.id}>
            {player.name}/{player.role}{" "}
            <button onClick={() => setEditingPlayer(player)}>Edit</button>
            <button onClick={() => handleDelete(player.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {!editingPlayer && (
        <>
          <h2>Add Player</h2>
          <Formik
            initialValues={{ name: "", role: "" }}
            validationSchema={playerSchema}
            onSubmit={handleAddPlayer}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <div>
                  <label htmlFor="role">Role:</label>
                  <Field as="select" id="role" name="role">
                    <option value="">Select Role</option>
                    <option value="Game Master">Game Master</option>
                    <option value="Player Character/Barbarian">
                      Barbarian
                    </option>
                    <option value="Player Character/Bard">Bard</option>
                    <option value="Player Character/Cleric">Cleric</option>
                    <option value="Player Character/Druid">Druid</option>
                    <option value="Player Character/Fighter">Fighter</option>
                    <option value="Player Character/Monk">Monk</option>
                    <option value="Player Character/Paladin">Paladin</option>
                    <option value="Player Character/Ranger">Ranger</option>
                    <option value="Player Character/Rogue">Rogue</option>
                    <option value="Player Character/Warlock">Warlock</option>
                    <option value="Player Character/Wizard">Wizard</option>
                  </Field>
                  <ErrorMessage name="role" component="div" />
                </div>
                <button type="submit">Add Player</button>
              </Form>
            )}
          </Formik>
        </>
      )}

      {editingPlayer && (
        <>
          <h2>Edit Player</h2>
          <Formik
            initialValues={{
              name: editingPlayer.name,
              role: editingPlayer.role,
            }}
            validationSchema={playerSchema}
            onSubmit={handleEditPlayer}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <div>
                  <label htmlFor="role">Role:</label>
                  <Field as="select" id="role" name="role">
                    <option value="">Select Role</option>
                    <option value="Player Character/Barbarian">
                      Barbarian
                    </option>
                    <option value="Player Character/Bard">Bard</option>
                    <option value="Player Character/Cleric">Cleric</option>
                    <option value="Player Character/Druid">Druid</option>
                    <option value="Player Character/Fighter">Fighter</option>
                    <option value="Player Character/Monk">Monk</option>
                    <option value="Player Character/Paladin">Paladin</option>
                    <option value="Player Character/Ranger">Ranger</option>
                    <option value="Player Character/Rogue">Rogue</option>
                    <option value="Player Character/Warlock">Warlock</option>
                    <option value="Player Character/Wizard">Wizard</option>
                  </Field>
                  <ErrorMessage name="role" component="div" />
                </div>
                <button type="submit">Save Changes</button>
                <button type="button" onClick={() => setEditingPlayer(null)}>
                  Cancel
                </button>
              </Form>
            )}
          </Formik>
        </>
      )}
    </div>
  );
}

export default PlayersPage;
