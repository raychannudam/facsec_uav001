<template>
    <div class="w-full grid grid-cols-12 gap-3">
        <div class="col-span-7">
            <LiveStreamView :key="triggerConfigUpdate" :drone-location="currentDroneLocation" />
        </div>

        <div class="col-span-5 flex flex-col space-y-3">
            <ControlPanelView />
            <!-- <button data-modal-target="openConfigurationModal" data-modal-toggle="openConfigurationModal"
                class="flex flex-row space-x-2 text-sm py-1 items-center px-4 hover:bg-blue-500 rounded-full border-blue-500 border dark:text-white hover:text-white self-end">
                <span class="material-symbols-outlined text-sm">tune</span>
                <p>Open Config</p>
            </button> -->
        </div>

        <!-- <div class="col-span-6">
            <ConfigurationView @onUpdate="updateConfig" />
        </div> -->

        <transition name="button">
            <button data-modal-target="openConfigurationModal" data-modal-toggle="openConfigurationModal"
                class="fixed m-8 bottom-16 right-0 bg-blue-600 dark:bg-blue-700 hover:bg-blue-700 dark:hover:bg-blue-600 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg transition-all hover:scale-110">
                <span class="material-symbols-outlined">
                    tune
                </span>
            </button>
        </transition>

        <PopupModalComponent id="openConfigurationModal" :show-footer="false">
            <template v-slot:header>
                <!-- Header -->
                <div class="flex flex-col w-full space-y-3">
                    <!-- Title + Description -->
                    <div class="flex flex-row items-center justify-between">
                        <div class="flex flex-col space-y-3">
                            <div class="flex flex-row items-center space-x-2">
                                <span class="text-2xl material-symbols-outlined">settings_input_component</span>
                                <p class="text-xl font-bold">Configuration</p>
                            </div>
                            <p class="text-xs text-gray-600 dark:text-gray-400 leading-tight">
                                Manage your control panel profiles.
                            </p>
                        </div>
                    </div>
                </div>
            </template>
            <template v-slot:body>
                <ConfigurationView @onUpdate="updateConfig" />
            </template>
        </PopupModalComponent>

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
import PopupModalComponent from '@/components/utils/PopupModalComponent.vue';

const controllerStore = useControllerStore();
const mqttStore = useMqttStore();
const triggerConfigUpdate = ref(0);
const currentDroneLocation = ref(null);
const currentSubscribedTopic = ref(null);
const isConnecting = ref(false);

onMounted(() => {
    document.title = 'Controller | DRSYS';
    initFlowbite();
});

const connectToMqtt = (controller) => {
    if (!controller?.config?.selectedDrone?.mqtt_client) return;
    if (isConnecting.value) return;
    const mqttConfig = controller.config.selectedDrone.mqtt_client;
    const brokerUrl = process.env.VUE_APP_MQTT_BROKER;
    const options = {
        username: mqttConfig.username,
        password: mqttConfig.raw_password,
        reconnectPeriod: 1000,
        keepalive: 30,
        clean: true,
    };
    if (mqttStore.isConnected) return;
    isConnecting.value = true;
    if (mqttStore.mqttClient) mqttStore.disconnect();
    mqttStore.connect(brokerUrl, options);
    setTimeout(() => {
        isConnecting.value = false;
    }, 2000);
};

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

watch(
    () => controllerStore.selectedController,
    (controller) => {
        if (controller?.config?.selectedDrone) {
            connectToMqtt(controller);
        }
    },
    { immediate: true, deep: true }
);

watch(() => mqttStore.isConnected, (isConnected) => {
    if (isConnected && controllerStore.selectedController) {
        subscribeToDroneLocation(controllerStore.selectedController);
    }
});

onBeforeUnmount(() => {
    if (currentSubscribedTopic.value && mqttStore.isConnected && mqttStore.mqttClient) {
        mqttStore.unsubscribe(currentSubscribedTopic.value);
    }
    setTimeout(() => {
        mqttStore.disconnect();
    }, 100);
});

const updateConfig = async () => {
    triggerConfigUpdate.value++;
    await controllerStore.getAllControllers();
};
</script>