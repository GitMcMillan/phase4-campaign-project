import React, { useState } from "react";
import { Formik, Form, Field, ErrorMessage } from "formik";
import * as Yup from "yup";

function CharactersPage({ characters, setCharacters }) {
  const [editingCharacter, setEditingCharacter] = useState(null);

  // validation schema
  const characterSchema = Yup.object().shape({
    name: Yup.string().required("Character name is required"),
    level: Yup.number()
      .required("Level is required")
      .min(1, "Level must be at least 1")
      .max(20, "Level cannot exceed 20"),
    character_class: Yup.string().required("Character class is required"),
  });

  //post
  const handleAddCharacter = (values, { resetForm }) => {
    fetch("http://127.0.0.1:5555/characters", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((newCharacter) => {
        setCharacters((prev) => [...prev, newCharacter]);
        resetForm();
      });
  };

  //patch
  const handleEditCharacter = (values) => {
    fetch(`http://127.0.0.1:5555/characters/${editingCharacter.id}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    })
      .then((res) => res.json())
      .then((updatedCharacter) => {
        setCharacters((prev) =>
          prev.map((character) =>
            character.id === updatedCharacter.id ? updatedCharacter : character
          )
        );
        setEditingCharacter(null);
      });
  };

  // delete
  const handleDelete = (id) => {
    fetch(`http://127.0.0.1:5555/characters/${id}`, {
      method: "DELETE",
    }).then(() => {
      setCharacters((prev) => prev.filter((character) => character.id !== id));
    });
  };

  return (
    <div>
      <h1>Characters</h1>
      <ul>
        {characters.map((character) => (
          <li key={character.id}>
            {character.name} - Level {character.level} (
            {character.character_class}){" "}
            <button onClick={() => setEditingCharacter(character)}>Edit</button>
            <button onClick={() => handleDelete(character.id)}>Delete</button>
          </li>
        ))}
      </ul>

      {!editingCharacter && (
        <>
          <h2>Add Character</h2>
          <Formik
            initialValues={{ name: "", level: "", character_class: "" }}
            validationSchema={characterSchema}
            onSubmit={handleAddCharacter}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <div>
                  <label htmlFor="level">Level:</label>
                  <Field id="level" name="level" type="number" />
                  <ErrorMessage name="level" component="div" />
                </div>
                <div>
                  <label htmlFor="character_class">Class:</label>
                  <Field id="character_class" name="character_class" />
                  <ErrorMessage name="character_class" component="div" />
                </div>
                <button type="submit">Add Character</button>
              </Form>
            )}
          </Formik>
        </>
      )}

      {editingCharacter && (
        <>
          <h2>Edit Character</h2>
          <Formik
            initialValues={{
              name: editingCharacter.name,
              level: editingCharacter.level,
              character_class: editingCharacter.character_class,
            }}
            validationSchema={characterSchema}
            onSubmit={handleEditCharacter}
          >
            {() => (
              <Form>
                <div>
                  <label htmlFor="name">Name:</label>
                  <Field id="name" name="name" />
                  <ErrorMessage name="name" component="div" />
                </div>
                <div>
                  <label htmlFor="level">Level:</label>
                  <Field id="level" name="level" type="number" />
                  <ErrorMessage name="level" component="div" />
                </div>
                <div>
                  <label htmlFor="character_class">Class:</label>
                  <Field id="character_class" name="character_class" />
                  <ErrorMessage name="character_class" component="div" />
                </div>
                <button type="submit">Save Changes</button>
                <button type="button" onClick={() => setEditingCharacter(null)}>
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

export default CharactersPage;
