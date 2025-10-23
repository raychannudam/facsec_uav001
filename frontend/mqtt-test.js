import mqtt from "mqtt";

// Change this to your MQTT broker URL
// For example: 'mqtt://localhost:1883' or 'wss://broker.hivemq.com:8884/mqtt'
const brokerUrl = 'wss://mqtt-broker.aitips.digital';

// Optional username/password if needed
const options = {
  clientId: 'mqtt_test_' + Math.random().toString(16).substring(2, 8),
  username: 'test1', // add if required
  password: 'test1', // add if required
  connectTimeout: 5000,
};

// Connect to broker
const client = mqtt.connect(brokerUrl, options);

let topic = "drsys/test1/1"

client.on('connect', () => {
  console.log('✅ Connected to MQTT broker');
  // Subscribe to a test topic
  client.subscribe(`${topic}`, (err) => {
    if (!err) {
      console.log(`📡 Subscribed to topic: ${topic}`);
    }
  });
});

client.on('message', (topic, message) => {
  console.log(`📥 Received message on ${topic}: ${message.toString()}`);
});

client.on('error', (err) => {
  console.error('❌ Connection error:', err);
});

client.on('close', () => {
  console.log('🔌 Disconnected from MQTT broker');
});

setInterval(()=>{
  client.publish(`${topic}`, 'Hello MQTT!');
  console.log("Published")
},1000)
