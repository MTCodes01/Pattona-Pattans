import React from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Register the required chart components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const EnergyLineChart = ({ data, title }) => {
  // Prepare data for the chart
  const chartData = {
    labels: data.map((entry) => entry.time), // Time labels
    datasets: [
      {
        label: "Energy Usage (kWh)",
        data: data.map((entry) => entry.usage), // Energy usage values
        borderColor: "rgba(75,192,192,1)", // Line color
        backgroundColor: "rgba(75,192,192,0.2)", // Area fill color
        borderWidth: 2,
        pointRadius: 3,
        tension: 0.4, // Smooth line
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: true,
        position: "top",
      },
      title: {
        display: true,
        text: title,
      },
    },
    scales: {
      x: {
        title: {
          display: true,
          text: "Time",
        },
      },
      y: {
        title: {
          display: true,
          text: "Energy Usage (kWh)",
        },
        beginAtZero: true,
      },
    },
  };

  return <Line data={chartData} options={options} />;
};

export default EnergyLineChart;
