import React from 'react';
import './About.css';

const About = () => {
  return (
    <div className="about-container">
      <h1>About the Energy Consumption Tracker</h1>

      <section className="problem-section">
        <h2>The Problem</h2>
        <p>
          The escalating energy consumption in households and workplaces is a significant contributor 
          to environmental degradation and high utility expenses. Despite the availability of energy 
          monitoring solutions, they often lack precision, real-time insights, and actionable recommendations, 
          making it difficult for users to optimize their energy usage effectively.
        </p>
      </section>

      <section className="solution-section">
        <h2>The Solution</h2>
        <p>
          The Energy Consumption Tracker offers an integrated solution for monitoring, analyzing, and optimizing 
          energy usage in real-time. Combining innovative IoT hardware, intuitive software interfaces, and data-driven 
          analytics, it empowers users to track and reduce their energy consumption. By providing granular insights 
          and actionable recommendations, the system facilitates cost savings, sustainability, and efficient energy management.
        </p>
      </section>

      <section className="impact-section">
        <h2>Impact</h2>
        <ul>
          <li><strong>Environmental Benefits:</strong> Promotes energy conservation, reducing carbon footprints, and aligns with global sustainability goals.</li>
          <li><strong>Economic Advantages:</strong> Reduces energy costs through informed decision-making and optimized usage patterns.</li>
          <li><strong>User Empowerment:</strong> Provides actionable insights with room-level and device-specific energy tracking, predictive analytics for proactive management.</li>
          <li><strong>Scalable Market Potential:</strong> Benefits residential, corporate, and industrial sectors, with opportunities for partnerships with energy providers and IoT manufacturers.</li>
        </ul>
      </section>

      <section className="features-section">
        <h2>Core Model Features</h2>
        <ul>
          <li><strong>Hardware Options:</strong> Centralized or distributed nodes for comprehensive tracking with IoT modules (ESP32/Arduino) and energy measurement sensors.</li>
          <li><strong>Software (Frontend & Backend):</strong> Real-time dashboards, alerts, and interactive analytics (built with React.js), predictive analytics and secure data processing (Python, Flask/Django).</li>
          <li><strong>Data Management:</strong> Time-series data storage for detailed insights (InfluxDB/MongoDB), secure communication via MQTT/HTTP protocols.</li>
          <li><strong>User-Focused Analytics:</strong> AI-powered usage recommendations, notifications for abnormal energy patterns and savings opportunities.</li>
        </ul>
      </section>

      <section className="future-enhancements-section">
        <h2>Future Enhancements</h2>
        <ul>
          <li><strong>AI Integration:</strong> Predictive models for usage optimization and anomaly detection.</li>
          <li><strong>Energy Sharing Platforms:</strong> Enabling users to share surplus renewable energy.</li>
          <li><strong>Mobile Accessibility:</strong> Native Android and iOS applications for real-time monitoring.</li>
        </ul>
      </section>

     
    </div>
  );
};

export default About;
