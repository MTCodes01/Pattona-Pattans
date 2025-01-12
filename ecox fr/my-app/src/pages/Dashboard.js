import React, { useState, useEffect } from "react";
import "./Dashboard.css";
import EnergyLineChart from "../components/EnergyLineChart";

const initialData = [
  {
    name: "Home",
    type: "Home",
    children: [
      {
        name: "Room1",
        type: "Room",
        children: [
          { name: "Bulb1", type: "Bulb", status: "Off", schedule: [] },
          { name: "Fan1", type: "Fan", status: "On", schedule: [] },
        ],
      },
      {
        name: "Room2",
        type: "Room",
        children: [
          { name: "Light1", type: "Light", status: "Off", schedule: [] },
          { name: "AC1", type: "AC", status: "On", schedule: [] },
        ],
      },
    ],
  },
];

const Dashboard = () => {
  const [data, setData] = useState(initialData);
  const [expandedNodes, setExpandedNodes] = useState([]);
  const [selectedNode, setSelectedNode] = useState("Home");
  const [newRoomName, setNewRoomName] = useState("");
  const [newDeviceName, setNewDeviceName] = useState({});
  const [energyUsageData, setEnergyUsageData] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (selectedNode) {
      fetchEnergyUsageData(selectedNode);
    }
  }, [selectedNode]);

  const fetchEnergyUsageData = async (nodeName) => {
    setLoading(true);
    try {
      const simulatedData = {
        Home: [
          { time: "10:00", usage: 20 },
          { time: "11:00", usage: 25 },
          { time: "12:00", usage: 22 },
        ],
        Room1: [
          { time: "10:00", usage: 8 },
          { time: "11:00", usage: 10 },
          { time: "12:00", usage: 12 },
        ],
        Room2: [
          { time: "10:00", usage: 12 },
          { time: "11:00", usage: 15 },
          { time: "12:00", usage: 14 },
        ],
        Bulb1: [
          { time: "10:00", usage: 1.5 },
          { time: "11:00", usage: 1.8 },
          { time: "12:00", usage: 1.3 },
        ],
        Fan1: [
          { time: "10:00", usage: 2.5 },
          { time: "11:00", usage: 2.8 },
          { time: "12:00", usage: 3.0 },
        ],
      };

      setEnergyUsageData(simulatedData[nodeName] || []);
    } catch (error) {
      console.error("Error fetching energy usage data:", error);
    } finally {
      setLoading(false);
    }
  };

  const toggleNode = (nodeName) => {
    setExpandedNodes((prev) =>
      prev.includes(nodeName)
        ? prev.filter((name) => name !== nodeName)
        : [...prev, nodeName]
    );
    setSelectedNode(nodeName);
  };

  const addRoom = () => {
    if (newRoomName.trim() === "") return;

    const updatedData = [...data];
    const homeNode = updatedData.find((node) => node.name === "Home");

    if (homeNode) {
      homeNode.children.push({
        name: newRoomName.trim(),
        type: "Room",
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
            status: "Off",
            schedule: [],
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

  const toggleDeviceStatus = (deviceName) => {
    const updateStatus = (nodes) => {
      return nodes.map((node) => {
        if (node.name === deviceName) {
          return { ...node, status: node.status === "On" ? "Off" : "On" };
        } else if (node.children) {
          return { ...node, children: updateStatus(node.children) };
        }
        return node;
      });
    };

    setData(updateStatus(data));
  };

  const renderTree = (nodes) => {
    return nodes.map((node) => {
      const isExpanded = expandedNodes.includes(node.name);
      const hasChildren = node.children && node.children.length > 0;

      return (
        <div key={node.name} className="tree-node">
          <div className="tree-label">
            <span
              onClick={() =>
                hasChildren ? toggleNode(node.name) : setSelectedNode(node.name)
              }
            >
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
                    setNewDeviceName((prev) => ({
                      ...prev,
                      [node.name]: e.target.value,
                    }))
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

  const selectedNodeDetails = (() => {
    const findNode = (nodes, name) => {
      for (let node of nodes) {
        if (node.name === name) return node;
        if (node.children) {
          const found = findNode(node.children, name);
          if (found) return found;
        }
      }
      return null;
    };

    return findNode(data, selectedNode);
  })();

  const getRoomDetails = (room) => {
    if (!room || !room.children) return { count: 0, types: [] };

    const types = room.children.map((device) => device.type);
    return { count: room.children.length, types: [...new Set(types)] };
  };

  return (
    <div className="dashboard">
      <h1>Energy Consumption Dashboard</h1>

      <div className="dashboard-container">
        {/* Tree View */}
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

        {/* Chart Section */}
        <div className="chart-section">
          {loading ? (
            <p>Loading chart data...</p>
          ) : energyUsageData.length > 0 ? (
            <EnergyLineChart
              data={energyUsageData}
              title={`Energy Usage for ${selectedNode}`}
            />
          ) : (
            <p>Select a node to view energy usage.</p>
          )}
        </div>

        {/* Info Box */}
        <div className="info-box">
          <h3>{selectedNode}</h3>
          {selectedNodeDetails && selectedNodeDetails.type === "Room" && (
            <>
              <p>
                Devices:{" "}
                {getRoomDetails(selectedNodeDetails).count || "No devices"}
              </p>
              <p>Types: {getRoomDetails(selectedNodeDetails).types.join(", ")}</p>
            </>
          )}
          {selectedNodeDetails && selectedNodeDetails.type !== "Room" && (
            <>
              <p>Type: {selectedNodeDetails.type}</p>
              <p>Status: {selectedNodeDetails.status}</p>
              <button
                onClick={() => toggleDeviceStatus(selectedNode)}
                className="status-toggle"
              >
                {selectedNodeDetails.status === "On" ? "Turn Off" : "Turn On"}
              </button>
            </>
          )}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
