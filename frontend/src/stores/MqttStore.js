import { defineStore } from "pinia";
import { ref } from "vue";
import mqtt from "mqtt";

export const useMqttStore = defineStore("mqtt", () => {
  // State
  const mqttClient = ref(null);
  const isConnected = ref(false);

  // Actions
  const connect = (brokerUrl, options) => {
    if (mqttClient.value) mqttClient.value.end();

    mqttClient.value = mqtt.connect(brokerUrl, options);

    mqttClient.value.on("connect", () => {
      console.log("✅ Connected to MQTT broker");
      isConnected.value = true;
    });

    mqttClient.value.on("error", (err) => {
      console.error("❌ MQTT Connection error:", err);
      isConnected.value = false;
    });

    mqttClient.value.on("close", () => {
      console.log("🔌 MQTT Connection closed");
      isConnected.value = false;
    });
  };

  const subscribe = (topic, callback) => {
    if (!mqttClient.value || !isConnected.value) {
      console.warn("⚠️ MQTT client not connected. Cannot subscribe.");
      return;
    }

    // Subscribe to the topic
    mqttClient.value.subscribe(topic, (err) => {
      if (!err) {
        console.log(`📡 Subscribed to topic: ${topic}`);
      } else {
        console.error(`❌ Failed to subscribe to ${topic}:`, err);
      }
    });

    // Listen for messages on this topic
    mqttClient.value.on("message", (receivedTopic, message) => {
      if (receivedTopic === topic && callback) {
        callback(message);
      }
    });
  };

  const publish = (topic, message) => {
    if (mqttClient.value && isConnected.value) {
      mqttClient.value.publish(topic, message);
      console.log(`📤 Published to ${topic}`);
    } else {
      console.warn("⚠️ MQTT client not connected. Cannot publish.");
    }
  };

  const disconnect = () => {
    if (mqttClient.value) {
      mqttClient.value.end();
      mqttClient.value = null;
      isConnected.value = false;
      console.log("👋 MQTT client disconnected");
    }
  };

  return {
    mqttClient,
    isConnected,
    connect,
    subscribe,
    publish,
    disconnect,
  };
});
