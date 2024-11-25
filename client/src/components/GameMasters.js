import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

function GameMastersPage({ gamemasters, setGameMasters }) {
  const [editingGameMaster, setEditingGameMaster] = useState(null);

  // validation
  const gameMasterSchema = Yup.object().shape({
    name: Yup.string().required("Game Master name is required"),
  });

  // post
  const handleAddGameMaster = (values, { resetForm }) => {
    fetch("http://127.0.0.1:5555/gamemasters", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((newGameMaster) => {
        setGameMasters((prev) => [...prev, newGameMaster]);
        resetForm();
      });
  };

  // patch
  const handleEditGameMaster = (values) => {
    fetch(`http://127.0.0.1:5555/gamemasters/${editingGameMaster.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((updatedGameMaster) => {
        setGameMasters((prev) =>
          prev.map((gm) =>
            gm.id === updatedGameMaster.id ? updatedGameMaster : gm
          )
        );
        setEditingGameMaster(null);
      });
  };

  // delet
  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5555/gamemasters/${id}`, {
      method: "DELETE",
    }).then(() => {
      setGameMasters((prev) => prev.filter((gm) => gm.id !== id));
    });
  };

  return (
    <div>
      <h1>Game Masters</h1>
      <ul>
        {gamemasters.map((gm) => (
          <li key={gm.id}>
            {gm.name}{" "}
            <button onClick={() => setEditingGameMaster(gm)}>Edit</button>
            <button onClick={() => handleDelete(gm.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {!editingGameMaster && (
        <>
          <h2>Add Game Master</h2>
          <Formik
            initialValues={{ name: "" }}
            validationSchema={gameMasterSchema}
            onSubmit={handleAddGameMaster}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <button type="submit">Add Game Master</button>
              </Form>
            )}
          </Formik>
        </>
      )}

      {editingGameMaster && (
        <>
          <h2>Edit Game Master</h2>
          <Formik
            initialValues={{ name: editingGameMaster.name }}
            validationSchema={gameMasterSchema}
            onSubmit={handleEditGameMaster}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <button type="submit">Save Changes</button>
                <button
                  type="button"
                  onClick={() => setEditingGameMaster(null)}
                >
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

export default GameMastersPage;
