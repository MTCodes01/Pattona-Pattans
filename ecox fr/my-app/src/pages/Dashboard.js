import React, { useState } from "react";
import "./Dashboard.css";
import EnergyLineChart from "../components/EnergyLineChart";

const initialData = [
  {
    name: "Home",
    children: [
      {
        name: "Room1",
        children: [
          { name: "Bulb1", type: "Light", energyUsage: [12, 15, 10, 8], status: "off" },
          { name: "Fan1", type: "Fan", energyUsage: [20, 25, 22, 18], status: "on" },
        ],
      },
      {
        name: "Room2",
        children: [
          { name: "Light1", type: "Light", energyUsage: [8, 10, 12, 9], status: "off" },
          { name: "AC1", type: "AC", energyUsage: [50, 55, 52, 48], status: "on" },
        ],
      },
    ],
  },
];

const Dashboard = () => {
  const [data, setData] = useState(initialData);
  const [expandedNodes, setExpandedNodes] = useState(["Home"]);
  const [selectedDevice, setSelectedDevice] = useState(null);
  const [newRoomName, setNewRoomName] = useState("");
  const [newDeviceName, setNewDeviceName] = useState({});

  const toggleNode = (nodeName) => {
    setExpandedNodes((prev) =>
      prev.includes(nodeName)
        ? prev.filter((name) => name !== nodeName)
        : [...prev, nodeName]
    );
  };

  const addRoom = () => {
    if (newRoomName.trim() === "") return;

    const updatedData = [...data];
    const homeNode = updatedData.find((node) => node.name === "Home");

    if (homeNode) {
      homeNode.children.push({
        name: newRoomName.trim(),
        children: [],
      });
    }

    setData(updatedData);
    setNewRoomName("");
    if (!expandedNodes.includes("Home")) {
      setExpandedNodes((prev) => [...prev, "Home"]);
    }
  };

  const addDevice = (roomName) => {
    if (!newDeviceName[roomName] || newDeviceName[roomName].trim() === "") return;

    const updatedData = [...data];

    const findAndAddDevice = (nodes) => {
      for (let node of nodes) {
        if (node.name === roomName) {
          if (!node.children) node.children = [];
          node.children.push({
            name: newDeviceName[roomName].trim(),
            type: "Unknown",
            energyUsage: [],
            status: "off",
          });
          return true;
        }
        if (node.children) findAndAddDevice(node.children);
      }
    };

    findAndAddDevice(updatedData);
    setData(updatedData);
    setNewDeviceName((prev) => ({ ...prev, [roomName]: "" }));
  };

  const toggleDeviceStatus = () => {
    if (!selectedDevice) return;

    const updateStatus = (nodes) => {
      return nodes.map((node) => {
        if (node.name === selectedDevice.name) {
          return { ...node, status: node.status === "on" ? "off" : "on" };
        }
        if (node.children) {
          return { ...node, children: updateStatus(node.children) };
        }
        return node;
      });
    };

    setData(updateStatus(data));
    setSelectedDevice((prev) => ({ ...prev, status: prev.status === "on" ? "off" : "on" }));
  };

  const renderTree = (nodes) => {
    return nodes.map((node) => {
      const isExpanded = expandedNodes.includes(node.name);
      const hasChildren = node.children && node.children.length > 0;

      return (
        <div key={node.name} className="tree-node">
          <div className={`tree-label ${hasChildren ? "clickable" : ""}`}>
            <span onClick={() => (hasChildren ? toggleNode(node.name) : setSelectedDevice(node))}>
              {node.name} {hasChildren && (isExpanded ? "-" : "+")}
            </span>
          </div>

          {hasChildren && isExpanded && (
            <div className="tree-children">
              {renderTree(node.children)}
              <div className="add-child">
                <input
                  type="text"
                  placeholder={`Add device to ${node.name}`}
                  value={newDeviceName[node.name] || ""}
                  onChange={(e) =>
                    setNewDeviceName((prev) => ({ ...prev, [node.name]: e.target.value }))
                  }
                />
                <button onClick={() => addDevice(node.name)}>Add Device</button>
              </div>
            </div>
          )}
        </div>
      );
    });
  };

  return (
    <div className="dashboard">
      <h1>Energy Consumption Dashboard</h1>

      <div className="dashboard-container">
        <div className="tree-view">
          <h2>Devices</h2>
          {renderTree(data)}

          <div className="add-room">
            <input
              type="text"
              placeholder="Enter new room name"
              value={newRoomName}
              onChange={(e) => setNewRoomName(e.target.value)}
            />
            <button onClick={addRoom}>Add Room</button>
          </div>
        </div>

        <div className="info-box">
          <h3>{selectedDevice ? selectedDevice.name : "Home"}</h3>
          <p>
            {selectedDevice
              ? `Type: ${selectedDevice.type || "Unknown"}, Status: ${selectedDevice.status}`
              : "View energy usage and device details here."}
          </p>
          {selectedDevice && (
            <button onClick={toggleDeviceStatus} className="toggle-button">
              {selectedDevice.status === "on" ? "Turn Off" : "Turn On"}
            </button>
          )}
        </div>

        <div className="chart-section">
          {selectedDevice && selectedDevice.energyUsage ? (
            <EnergyLineChart
              data={selectedDevice.energyUsage.map((usage, index) => ({
                time: `Hour ${index + 1}`,
                usage,
              }))}
              title={`Energy Usage for ${selectedDevice.name}`}
            />
          ) : (
            <p>Select a device to view energy usage.</p>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
