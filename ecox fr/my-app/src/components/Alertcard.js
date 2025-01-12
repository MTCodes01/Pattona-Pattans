function AlertCard({ message }) {
    return (
      <div style={styles.alertCard}>
        <p>{message}</p>
      </div>
    );
  }
  
  const styles = {
    alertCard: {
      backgroundColor: "#f8d7da",
      color: "#721c24",
      padding: "10px",
      margin: "10px 0",
      borderRadius: "5px",
      border: "1px solid #f5c6cb",
    },
  };
  
  export default AlertCard;
  