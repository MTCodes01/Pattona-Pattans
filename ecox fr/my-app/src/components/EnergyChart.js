function EnergyChart() {
    return (
      <div style={styles.chartContainer}>
        <h2>Energy Consumption Chart</h2>
        <p>Graph will be displayed here.</p>
      </div>
    );
  }
  
  const styles = {
    chartContainer: {
      textAlign: "center",
      margin: "20px",
      padding: "20px",
      border: "1px solid #ccc",
      borderRadius: "8px",
    },
  };
  
  export default EnergyChart;
  