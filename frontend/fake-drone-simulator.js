import mqtt from "mqtt";

// MQTT Broker configuration
const brokerUrl = "ws://localhost:9002";
const options = {
  username: "test",
  password: "test",
};

const client = mqtt.connect(brokerUrl, options);
const topic = "drsys/test/gps_latlng";

// Starting location (Phnom Penh, Cambodia)
let currentLat = 11.5564;
let currentLng = 104.9282;

// How much the drone moves each update (smaller = slower movement)
const MOVEMENT_SPEED = 0.001;

client.on("connect", () => {
  setInterval(() => {
    const latChange = (Math.random() - 0.5) * MOVEMENT_SPEED;
    const lngChange = (Math.random() - 0.5) * MOVEMENT_SPEED;

    currentLat += latChange;
    currentLng += lngChange;

    const locationText = `${currentLat.toFixed(6)},${currentLng.toFixed(6)}`;
    client.publish(topic, locationText);
  }, 5000);
});

client.on("error", (err) => {
  console.error("❌ Connection error:", err);
});

client.on("close", () => {
  console.log("🔌 Disconnected from MQTT broker");
});

// Handle process termination gracefully
process.on("SIGINT", () => {
  client.end();
  process.exit();
});
