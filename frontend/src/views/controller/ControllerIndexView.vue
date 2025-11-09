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

const controllerStore = useControllerStore();
const mqttStore = useMqttStore();
const triggerConfigUpdate = ref(0);
const currentDroneLocation = ref(null);

onMounted(() => {
    document.title = 'Controller | DRSYS';
    initFlowbite();
});

// Watch for selectedController changes and connect to MQTT when available
watch(
    () => controllerStore.selectedController,
    (controller) => {
        if (controller?.config?.selectedDrone?.mqtt_client) {
            const mqttConfig = controller.config.selectedDrone.mqtt_client;
            const brokerUrl = process.env.VUE_APP_MQTT_BROKER;
            const options = {
                username: mqttConfig.username,
                password: mqttConfig.raw_password,
            };
            console.log('🔌 Connecting to MQTT broker for drone tracking...');
            mqttStore.connect(brokerUrl, options);
        }
    },
    { immediate: true, deep: true }
);

watch(() => mqttStore.isConnected, (isConnected) => {
    if (isConnected) {
        const topic = controllerStore.selectedController?.config?.default?.mqttTopics[2].name;
        console.log("topic", topic)
        console.log(`🎯 Subscribing to drone location topic: ${topic}`);

        mqttStore.subscribe(topic, (message) => {
            try {
                const text = message.toString();
                const [latStr, lngStr] = text.split(",");
                currentDroneLocation.value = {
                    lat: parseFloat(latStr),
                    lng: parseFloat(lngStr),
                    timestamp: new Date()
                };
            } catch (error) {
                console.error('❌ Error parsing drone location:', error);
            }
        });
    }
});

onBeforeUnmount(() => {
    mqttStore.disconnect();
});

const updateConfig = () => {
    triggerConfigUpdate.value++;
};
</script>