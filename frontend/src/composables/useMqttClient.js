import { ref } from "vue";
import mqtt from "mqtt";

const mqttClient = ref(null);
const isConnected = ref(false);

export function useMqttClient() {
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
      isConnected.value = false;
    });
  };

  const publish = (topic, message) => {
    if (mqttClient.value && isConnected.value) {
      mqttClient.value.publish(topic, message);
    } else {
      console.warn("MQTT client not connected");
    }
  };

  const disconnect = () => {
    if (mqttClient.value) {
      mqttClient.value.end();
      mqttClient.value = null;
      isConnected.value = false;
    }
  };

  return {
    mqttClient,
    isConnected,
    connect,
    publish,
    disconnect,
  };
}
