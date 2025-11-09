import { defineStore } from "pinia";
import { ref } from "vue";
import mqtt from "mqtt";

export const useMqttStore = defineStore("mqtt", () => {
  // State
  const mqttClient = ref(null);
  const isConnected = ref(false);
  const topicCallbacks = ref({});

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

    // Setup message listener ONCE when connecting
    mqttClient.value.on("message", (receivedTopic, message) => {
      console.log(`📥 Message received on topic: ${receivedTopic}`);

      // Find and call the callback for this topic
      const callback = topicCallbacks.value[receivedTopic];
      if (callback) {
        callback(message);
      } else {
        console.warn(`⚠️ No callback registered for topic: ${receivedTopic}`);
      }
    });
  };

  const subscribe = (topic, callback) => {
    if (!mqttClient.value || !isConnected.value) {
      console.warn("⚠️ MQTT client not connected. Cannot subscribe.");
      return;
    }

    // Store the callback FIRST
    topicCallbacks.value[topic] = callback;
    console.log(`💾 Callback stored for topic: ${topic}`);

    // Then subscribe to the topic
    mqttClient.value.subscribe(topic, (err) => {
      if (!err) {
        console.log(`📡 Subscribed to topic: ${topic}`);
      } else {
        console.error(`❌ Failed to subscribe to ${topic}:`, err);
        // Remove callback if subscription failed
        delete topicCallbacks.value[topic];
      }
    });
  };

  const unsubscribe = (topic) => {
    if (!mqttClient.value) {
      console.warn("⚠️ MQTT client not available. Cannot unsubscribe.");
      return;
    }

    // Unsubscribe from the topic
    mqttClient.value.unsubscribe(topic, (err) => {
      if (!err) {
        console.log(`🔕 Unsubscribed from topic: ${topic}`);
        // Remove the callback
        delete topicCallbacks.value[topic];
      } else {
        console.error(`❌ Failed to unsubscribe from ${topic}:`, err);
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
      // Unsubscribe from all topics before disconnecting
      Object.keys(topicCallbacks.value).forEach((topic) => {
        mqttClient.value.unsubscribe(topic);
      });

      mqttClient.value.end();
      mqttClient.value = null;
      isConnected.value = false;
      topicCallbacks.value = {};
      console.log("👋 MQTT client disconnected");
    }
  };

  return {
    mqttClient,
    isConnected,
    connect,
    subscribe,
    unsubscribe, // <-- Don't forget to export this!
    publish,
    disconnect,
  };
});
