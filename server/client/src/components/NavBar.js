import React from "react";
import { Link } from "react-router-dom";

function NavBar() {
  return (
    <nav
      style={{
        padding: "10px",
        backgroundColor: "orange",
        borderBottom: "1px solid #ccc",
      }}
    >
      <Link to="/" style={{ margin: "0 10px" }}>
        Home
      </Link>
      <Link to="/characters" style={{ margin: "0 10px" }}>
        Character Info
      </Link>
      <Link to="/players" style={{ margin: "0 10px" }}>
        Player Info
      </Link>
      <Link to="/gamemasters" style={{ margin: "0 10px" }}>
        Game Master
      </Link>
    </nav>
  );
}

export default NavBar;
