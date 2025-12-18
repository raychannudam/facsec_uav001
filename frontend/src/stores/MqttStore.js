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

    const enhancedOptions = {
      ...options,
      keepalive: 30,
      clean: true,
      reconnectPeriod: 1000,
      connectTimeout: 30 * 1000,
      clientId: `mqtt_${Math.random().toString(16).substr(2, 8)}`,
    };

    mqttClient.value = mqtt.connect(brokerUrl, enhancedOptions);

    mqttClient.value.on("connect", () => {
      isConnected.value = true;
    });

    mqttClient.value.on("reconnect", () => {
      isConnected.value = false;
    });

    mqttClient.value.on("error", (err) => {
      console.error("MQTT Error:", err);
      isConnected.value = false;
    });

    mqttClient.value.on("close", () => {
      isConnected.value = false;
    });

    mqttClient.value.on("offline", () => {
      isConnected.value = false;
    });

    mqttClient.value.on("message", (receivedTopic, message) => {
      const callback = topicCallbacks.value[receivedTopic];
      if (callback) {
        callback(message);
      }
    });
  };

  const subscribe = (topic, callback) => {
    if (!mqttClient.value || !isConnected.value) {
      return;
    }

    topicCallbacks.value[topic] = callback;

    mqttClient.value.subscribe(topic, (err) => {
      if (err) {
        console.error(`Subscribe error: ${topic}`, err);
        delete topicCallbacks.value[topic];
      }
    });
  };

  const unsubscribe = (topic) => {
    if (!mqttClient.value || !mqttClient.value.connected) {
      delete topicCallbacks.value[topic];
      return;
    }

    mqttClient.value.unsubscribe(topic, (err) => {
      if (!err) {
        delete topicCallbacks.value[topic];
      }
    });
  };

  const publish = (topic, message) => {
    if (mqttClient.value && isConnected.value) {
      mqttClient.value.publish(topic, message, { qos: 1 });
    }
  };

  const disconnect = () => {
    if (mqttClient.value) {
      Object.keys(topicCallbacks.value).forEach((topic) => {
        mqttClient.value.unsubscribe(topic);
      });

      mqttClient.value.end();
      mqttClient.value = null;
      isConnected.value = false;
      topicCallbacks.value = {};
    }
  };

  return {
    mqttClient,
    isConnected,
    connect,
    subscribe,
    unsubscribe,
    publish,
    disconnect,
  };
});
