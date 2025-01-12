import React from "react";
import { Link } from "react-router-dom";
import "./Home.css"; // Import the CSS file

function Home() {
  return (
    <div className="home-container">
      {/* Header Section */}
      <header className="home-header">
        <h1>Welcome to Ecox</h1>
        <p>Your all-in-one solution for monitoring and optimizing energy usage.</p>
      </header>

      {/* Call-to-Action Buttons */}
      <div className="home-cta">
        <Link to="/dashboard" className="home-button">Get Started</Link>
        <Link to="/about" className="home-button-secondary">Learn More</Link>
      </div>

      {/* Footer */}
      <footer className="home-footer">
        <p>© 2025 Ecox. All Rights Reserved.</p>
      </footer>
    </div>
  );
}

export default Home;
