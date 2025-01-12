import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav style={styles.navbar}>
      <Link to="/" style={styles.link}>Home</Link>
      <Link to="/dashboard" style={styles.link}>Dashboard</Link>
      <Link to="/settings" style={styles.link}>Settings</Link>
    </nav>
  );
}

const styles = {
  navbar: {
    display: "flex",
    justifyContent: "space-around",
    padding: "10px",
    backgroundColor: "#282c34",
  },
  link: {
    color: "white",
    textDecoration: "none",
    fontSize: "18px",
  },
};

export default Navbar;
