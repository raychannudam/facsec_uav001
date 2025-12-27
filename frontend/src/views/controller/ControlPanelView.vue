<template>
    <div class="flex flex-col space-y-3 h-full text-sm">

        <div class="flex flex-row space-x-3 w-full items-end justify-between">
            <div class="text-2xl flex flex-col items-start space-y-3">
                <div class="flex font-bold flex-row space-x-3 items-center">
                    <span class="text-2xl material-symbols-outlined">
                        stadia_controller
                    </span>
                    <p>Control Panel</p>
                </div>
                <p class="text-gray-600 dark:text-gray-400 text-xs">
                    Real-time controller interface.
                </p>
            </div>
            <div class="flex items-center space-x-3 dark:text-gray-400 px-3">
                <!-- <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined text-sm">
                        battery_charging_full
                    </span>
                    <p>Batt, </p>
                    <p class="font-bold dark:text-white">{{ telemetryData.battery !== null ? telemetryData.battery + '%'
                        : '--' }}</p>
                </div>
                <div>|</div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined text-sm">
                        device_thermostat
                    </span>
                    <p>Temp, </p>
                    <p class="font-bold dark:text-white">{{ telemetryData.temperature !== null ?
                        telemetryData.temperature + '°C' : '--' }}</p>
                </div>
                <div>|</div> -->
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined text-sm">
                        speed
                    </span>
                    <p>Speed, </p>
                    <p class="font-bold dark:text-white">{{ telemetryData.speed !== null ? telemetryData.speed + ' m/s'
                        : '--' }}</p>
                </div>
                <div>|</div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined text-sm">
                        height
                    </span>
                    <p>Altitude, </p>
                    <p class="font-bold dark:text-white">{{ telemetryData.altitude !== null ? telemetryData.altitude +
                        'm' : '--' }}</p>
                </div>
            </div>
        </div>

        <hr class="border-0.5 border-gray-200">

        <!-- Show message if no profile selected -->
        <div v-if="!controllerStore.selectedController" class="text-center text-gray-500 dark:text-gray-400 py-8">
            No profile selected. Please select a profile in the Configuration panel.
        </div>

        <!-- New Grid Layout: 4 columns -->
        <div v-else class="grid grid-cols-1 lg:grid-cols-4 gap-4 mt-4">
            <!-- Buttons Section - 25% width (1 column) -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 flex flex-col">
                <div class="flex items-center gap-2 mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                    </svg>
                    <h3 class="text-sm font-bold text-gray-800 dark:text-white">Buttons</h3>
                </div>
                <div v-if="controllerStore.buttons.length > 0" class="space-y-2">
                    <ControlButton v-for="button in controllerStore.buttons" :key="button.id" :button="button"
                        @trigger="handleButtonClick" />
                </div>
                <div v-else class="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
                    No buttons configured
                </div>
            </div>


            <!-- Switches Section - 25% width (1 column) -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 flex flex-col">
                <div class="flex items-center gap-2 mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-green-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4" />
                    </svg>
                    <h3 class="text-sm font-bold text-gray-800 dark:text-white">Switches</h3>
                </div>
                <div v-if="controllerStore.switches.length > 0" class="space-y-2">
                    <ControlSwitch v-for="switchItem in controllerStore.switches" :key="switchItem.id"
                        :switchData="switchItem" @toggle="handleSwitchToggle" />
                </div>
                <div v-else class="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
                    No switches configured
                </div>
            </div>

            <!-- Sliders Section - 50% width (2 columns) -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 lg:col-span-2 flex flex-col">
                <div class="flex items-center gap-2 mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-purple-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M4 8V4m0 0h4M4 4l5 5m11-1V4m0 0h-4m4 0l-5 5M4 16v4m0 0h4m-4 0l5-5m11 5l-5-5m5 5v-4m0 4h-4" />
                    </svg>
                    <h3 class="text-sm font-bold text-gray-800 dark:text-white">Sliders</h3>
                </div>
                <div v-if="controllerStore.sliders.length > 0" class="space-y-2">
                    <ControlSlider v-for="slider in controllerStore.sliders" :key="slider.id" :slider="slider"
                        @change="handleSliderChange" />
                </div>
                <div v-else class="text-sm text-gray-500 dark:text-gray-400 text-center py-4">
                    No sliders configured
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch } from 'vue';
import ControlButton from '@/components/controller/ControlButton.vue';
import ControlSlider from '@/components/controller/ControlSlider.vue';
import ControlSwitch from '@/components/controller/ControlSwitch.vue';
import { useControllerStore } from '@/stores/ControllerStore';
import { useMqttStore } from '@/stores/MqttStore';

const controllerStore = useControllerStore();
const mqttStore = useMqttStore();
const { publish } = mqttStore;

const telemetryData = ref({
    altitude: null,
    battery: null,
    speed: null,
    temperature: null
});

const subscribedTelemetryTopics = ref([]);

// Define functions first before using them in watchers
const resetTelemetryData = () => {
    telemetryData.value = {
        altitude: null,
        battery: null,
        speed: null,
        temperature: null
    };
};

const unsubscribeFromTelemetry = () => {
    subscribedTelemetryTopics.value.forEach(topic => {
        mqttStore.unsubscribe(topic);
    });
    subscribedTelemetryTopics.value = [];
    resetTelemetryData();
};

const subscribeToTelemetry = () => {
    const controller = controllerStore.selectedController;

    if (!controller?.config?.default?.mqttTopics || !mqttStore.isConnected) {
        return;
    }

    const defaultTopics = controller.config.default.mqttTopics;

    const topicMap = {
        altitude: 'altitude',
        battery: 'battery',
        speed: 'speed',
        temperature: 'temperature'
    };

    Object.entries(topicMap).forEach(([key, searchTerm]) => {
        const topic = defaultTopics.find(t =>
            t.id?.toLowerCase() === searchTerm ||
            t.name?.toLowerCase().includes(searchTerm)
        );

        if (topic?.name) {

            mqttStore.subscribe(topic.name, (message) => {
                try {
                    const rawValue = message.toString().trim();
                    const value = parseFloat(rawValue);

                    if (!isNaN(value)) {
                        telemetryData.value[key] = value;
                    } else {
                        console.warn(`⚠️ Could not parse ${key} value:`, rawValue);
                    }
                } catch (error) {
                    console.error(`❌ Error parsing ${key}:`, error);
                }
            });

            subscribedTelemetryTopics.value.push(topic.name);
        } else {
            console.warn(`⚠️ No topic found for ${key} (searching for: ${searchTerm})`);
        }
    });
};

onMounted(async () => {
    await controllerStore.getAllControllers();

    // Subscribe to telemetry if MQTT is already connected
    if (mqttStore.isConnected && controllerStore.selectedController) {
        subscribeToTelemetry();
    }
});

onBeforeUnmount(() => {
    unsubscribeFromTelemetry();
});

// Watch for controller changes and log the controls
watch(
    () => controllerStore.selectedController,
    (newController) => {
        if (newController) {

            // Resubscribe to telemetry when controller changes
            unsubscribeFromTelemetry();
            if (mqttStore.isConnected) {
                subscribeToTelemetry();
            }
        }
    },
    { deep: true, immediate: true }
);

// Watch for MQTT connection status
watch(
    () => mqttStore.isConnected,
    (isConnected) => {
        if (isConnected && controllerStore.selectedController) {
            subscribeToTelemetry();
        } else if (!isConnected) {
            resetTelemetryData();
        }
    }
);

const handleButtonClick = (data) => {
    const button = controllerStore.buttons.find(b => b.id === data.id);
    if (button?.selectedTopic?.name) {
        publish(button.selectedTopic.name, String(data.payload));
    } else {
        console.warn('⚠️ Button has no topic configured:', data.id);
    }
};

const handleSwitchToggle = (data) => {
    const switchItem = controllerStore.switches.find(s => s.id === data.id);
    if (switchItem?.selectedTopic?.name) {
        publish(switchItem.selectedTopic.name, String(data.payload));
        controllerStore.updateMqttTopicAdditionalConfig(controllerStore.selectedController.id, switchItem.id, {
            "additionalConfig":{    
                "latest_state":  String(data.payload)
            }
        })
    } else {
        console.warn('⚠️ Switch has no topic configured:', data.id);
    }
};

const handleSliderChange = (data) => {
    const slider = controllerStore.sliders.find(s => s.id === data.id);
    if (slider?.selectedTopic?.name) {
        publish(slider.selectedTopic.name, String(data.value));
        controllerStore.updateMqttTopicAdditionalConfig(controllerStore.selectedController.id, slider.id, {
            "additionalConfig":{    
                "latest_state":  String(data.value)
            }
        })
    } else {
        console.warn('⚠️ Slider has no topic configured:', data.id);
    }
};
</script>