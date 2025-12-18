<template>
    <div class="w-full grid grid-cols-12 gap-3">
        <div class="col-span-8">
            <LiveStreamView :key="triggerConfigUpdate" :drone-location="currentDroneLocation" />
        </div>

        <div class="col-span-4">
            <ConfigurationView @onUpdate="updateConfig" />
        </div>

        <div class="col-span-12">
            <ControlPanelView />
        </div>

        <!-- Chatbot Component -->
        <ChatbotView />
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { initFlowbite } from 'flowbite';
import ConfigurationView from './ConfigurationView.vue';
import ControlPanelView from './ControlPanelView.vue';
import LiveStreamView from './LiveStreamView.vue';
import ChatbotView from './ChatbotView.vue';
import { useControllerStore } from '@/stores/ControllerStore';
import { useMqttStore } from '@/stores/MqttStore';

const controllerStore = useControllerStore();
const mqttStore = useMqttStore();
const triggerConfigUpdate = ref(0);
const currentDroneLocation = ref(null);
const currentSubscribedTopic = ref(null);

onMounted(() => {
    document.title = 'Controller | DRSYS';
    initFlowbite();
});

// Function to connect to MQTT with drone config
const connectToMqtt = (controller) => {
    if (!controller?.config?.selectedDrone?.mqtt_client) {
        return;
    }
    const mqttConfig = controller.config.selectedDrone.mqtt_client;
    const brokerUrl = process.env.VUE_APP_MQTT_BROKER;
    const options = {
        username: mqttConfig.username,
        password: mqttConfig.raw_password,
        reconnectPeriod: 1000,
    };
    if (mqttStore.isConnected) mqttStore.disconnect();
    mqttStore.connect(brokerUrl, options);
};

// Function to subscribe to drone location topic
const subscribeToDroneLocation = (controller) => {
    if (!mqttStore.isConnected) {
        return;
    }
    const defaultTopics = controller?.config?.default?.mqttTopics;
    if (!defaultTopics || defaultTopics.length === 0) {
        return;
    }
    const locationTopic = defaultTopics.find(
        topic => topic.name && (topic.name.toLowerCase().includes('gps') || topic.name.toLowerCase().includes('latlng'))
    );
    if (!locationTopic?.name) {
        return;
    }
    const topicName = locationTopic.name;

    // Unsubscribe from old topic if exists
    if (currentSubscribedTopic.value && currentSubscribedTopic.value !== topicName) {
        mqttStore.unsubscribe(currentSubscribedTopic.value);
    }

    currentSubscribedTopic.value = topicName;

    mqttStore.subscribe(topicName, (message) => {
        try {
            const text = message.toString();
            const [latStr, lngStr] = text.split("/");

            const lat = parseFloat(latStr);
            const lng = parseFloat(lngStr);

            if (!isNaN(lat) && !isNaN(lng)) {
                currentDroneLocation.value = {
                    droneId: controller?.config?.selectedDrone?.name || 'Unknown Drone',
                    lat,
                    lng,
                    altitude: controller?.config?.selectedDrone?.altitude,
                    battery: controller?.config?.selectedDrone?.battery,
                    timestamp: new Date()
                };
            }
        } catch (error) {
            console.error('❌ Error parsing drone location:', error);
        }
    });
};

// Watch for controller changes and reconnect MQTT
watch(
    () => controllerStore.selectedController,
    (controller) => {
        if (controller?.config?.selectedDrone) {
            connectToMqtt(controller);
        }
    },
    { immediate: true, deep: true }
);

// Watch for MQTT connection and subscribe to topic
watch(() => mqttStore.isConnected, (isConnected) => {
    if (isConnected && controllerStore.selectedController) {
        subscribeToDroneLocation(controllerStore.selectedController);
    }
});

onBeforeUnmount(() => {
    if (currentSubscribedTopic.value) {
        mqttStore.unsubscribe(currentSubscribedTopic.value);
    }
    mqttStore.disconnect();
});

const updateConfig = async () => {
    triggerConfigUpdate.value++;

    // Reload the controller to get fresh data
    await controllerStore.getAllControllers();
};
</script>