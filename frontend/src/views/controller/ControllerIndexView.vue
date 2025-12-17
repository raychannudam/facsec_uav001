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

        <ChatbotView />
    </div>
</template>

<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue';
import { initFlowbite } from 'flowbite';
import ConfigurationView from './ConfigurationView.vue';
import ControlPanelView from './ControlPanelView.vue';
import LiveStreamView from './LiveStreamView.vue';
import { useControllerStore } from '@/stores/ControllerStore';
import { useMqttStore } from '@/stores/MqttStore';
import ChatbotView from './ChatbotView.vue';

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
        console.log('⚠️ No MQTT client configured');
        return;
    }
    const mqttConfig = controller.config.selectedDrone.mqtt_client;
    const brokerUrl = process.env.VUE_APP_MQTT_BROKER;
    const options = {
        username: mqttConfig.username,
        password: mqttConfig.raw_password,
        reconnectPeriod: 1000,
    };
    console.log('🔌 Connecting to MQTT broker for drone tracking...');
    if (mqttStore.isConnected) mqttStore.disconnect();
    mqttStore.connect(brokerUrl, options);
};

// Function to subscribe to drone location topic
const subscribeToDroneLocation = (controller) => {
    if (!mqttStore.isConnected) {
        console.log('⚠️ MQTT not connected yet');
        return;
    }
    const defaultTopics = controller?.config?.default?.mqttTopics;
    if (!defaultTopics || defaultTopics.length === 0) {
        console.log('⚠️ No default topics configured');
        return;
    }
    const locationTopic = defaultTopics.find(
        topic => topic.name && (topic.name.toLowerCase().includes('gps') || topic.name.toLowerCase().includes('latlng'))
    );
    if (!locationTopic?.name) {
        console.log('⚠️ No GPS location topic found');
        console.log('Available default topics:', defaultTopics);
        return;
    }
    const topicName = locationTopic.name;
    console.log('📡 Subscribing to GPS topic:', topicName);

    // Unsubscribe from old topic if exists
    if (currentSubscribedTopic.value && currentSubscribedTopic.value !== topicName) {
        console.log(`📤 Unsubscribing from old topic: ${currentSubscribedTopic.value}`);
        mqttStore.unsubscribe(currentSubscribedTopic.value);
    }

    console.log(`🎯 Subscribing to drone location topic: ${topicName}`);
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
                console.log('📍 Drone location updated:', currentDroneLocation.value);
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
            console.log('🔄 Controller changed, reconnecting MQTT...');
            connectToMqtt(controller);
        }
    },
    { immediate: true, deep: true }
);

// Watch for MQTT connection and subscribe to topic
watch(() => mqttStore.isConnected, (isConnected) => {
    if (isConnected && controllerStore.selectedController) {
        console.log('✅ MQTT connected, subscribing to topics...');
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
    console.log('🔄 Configuration updated, reloading controller...');
    triggerConfigUpdate.value++;

    // Reload the controller to get fresh data
    await controllerStore.getAllControllers();

    // The watch on selectedController will handle reconnection
};
</script>