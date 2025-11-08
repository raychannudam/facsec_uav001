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
  console.log("✅ Fake Drone Connected to MQTT broker");
  console.log(`📍 Starting position: ${currentLat}, ${currentLng}`);
  console.log("🚁 Drone will update location every 5 seconds...\n");

  // Send location every 5 seconds
  setInterval(() => {
    // Simulate random drone movement
    // The drone will move in small random steps
    const latChange = (Math.random() - 0.5) * MOVEMENT_SPEED;
    const lngChange = (Math.random() - 0.5) * MOVEMENT_SPEED;

    currentLat += latChange;
    currentLng += lngChange;

    // Create location data object
    const locationData = {
      droneId: "DRONE-001",
      lat: currentLat,
      lng: currentLng,
      timestamp: new Date().toISOString(),
    };

    // Convert to JSON and publish
    client.publish(topic, JSON.stringify(locationData));

    // Log to console
    console.log("📤 Published location:");
    console.log(`   Drone: ${locationData.droneId}`);
    console.log(
      `   Position: ${locationData.lat.toFixed(6)}, ${locationData.lng.toFixed(
        6
      )}`
    );
    console.log(
      `   Time: ${new Date(locationData.timestamp).toLocaleTimeString()}\n`
    );
  }, 5000); // 5000 milliseconds = 5 seconds
});

client.on("error", (err) => {
  console.error("❌ Connection error:", err);
  console.log(
    "💡 Make sure your MQTT broker is running on ws://localhost:9002"
  );
});

client.on("close", () => {
  console.log("🔌 Disconnected from MQTT broker");
});

// Handle process termination gracefully
process.on("SIGINT", () => {
  console.log("\n👋 Stopping fake drone...");
  client.end();
  process.exit();
});
