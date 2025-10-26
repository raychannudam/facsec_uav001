<template>
    <div class="flex flex-col space-y-3">
        <div class="flex flex-row space-x-3 w-full items-end justify-between">
            <div class="text-2xl flex flex-col items-start space-y-3">
                <div class="flex font-bold flex-row space-x-3 items-center">
                    <span class="text-2xl material-symbols-outlined">
                        stadia_controller
                    </span>
                    <p>Control Panel</p>
                </div>
                <p class="text-gray-600 dark:text-gray-400 text-sm">
                    Get real-time live stream video from the cameras on the drone.
                </p>
            </div>
            <div class="flex items-center space-x-3 dark:text-gray-400 px-3">
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        device_thermostat
                    </span>
                    <p>Temp, </p>
                    <p class="font-bold dark:text-white">-- &#8451;</p>
                </div>
                <div>
                    |
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        speed
                    </span>
                    <p>Speed, </p>
                    <p class="font-bold dark:text-white">-- km/h</p>
                </div>
                <div>
                    |
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        altitude
                    </span>
                    <p>Altitude, </p>
                    <p class="font-bold dark:text-white">---- m</p>
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        timer
                    </span>
                    <p>Time, </p>
                    <p class="font-bold dark:text-white">-- mn</p>
                </div>
            </div>
        </div>
        <hr class="border-0.5 border-gray-200">

        <!-- New Grid Layout: 4 columns -->
        <div class="grid grid-cols-1 lg:grid-cols-4 gap-4 mt-4">
            <!-- Buttons Section - 25% width (1 column) -->
            <div class="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-4 flex flex-col">
                <div class="flex items-center gap-2 mb-4">
                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-blue-600" fill="none"
                        viewBox="0 0 24 24" stroke="currentColor">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 2.239l.777 2.897M5.136 7.965l-2.898-.777M13.95 4.05l-2.122 2.122m-5.657 5.656l-2.12 2.122" />
                    </svg>
                    <h3 class="text-lg font-bold text-gray-800 dark:text-white">Buttons</h3>
                </div>
                <div class="space-y-2">
                    <ControlButton v-for="button in controllerStore.buttons" :key="button.id" :button="button"
                        @trigger="handleButtonClick" />
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
                    <h3 class="text-lg font-bold text-gray-800 dark:text-white">Switches</h3>
                </div>
                <div class="space-y-2">
                    <ControlSwitch v-for="switchItem in controllerStore.switches" :key="switchItem.id"
                        :switchData="switchItem" @toggle="handleSwitchToggle" />
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
                    <h3 class="text-lg font-bold text-gray-800 dark:text-white">Sliders</h3>
                </div>
                <div class="space-y-2">
                    <ControlSlider v-for="slider in controllerStore.sliders" :key="slider.id" :slider="slider"
                        @change="handleSliderChange" />
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { onMounted } from 'vue';
import ControlButton from '@/components/controller/ControlButton.vue';
import ControlSlider from '@/components/controller/ControlSlider.vue';
import ControlSwitch from '@/components/controller/ControlSwitch.vue';
import { useControllerStore } from '@/stores/ControllerStore';
import { useMqttClient } from '@/composables/useMqttClient';

const controllerStore = useControllerStore();
const { publish, isConnected } = useMqttClient();

onMounted(async () => {
    await controllerStore.getAllControllers();
});

const handleButtonClick = (data) => {
    const button = controllerStore.buttons.find(b => b.id === data.id);
    if (button?.selectedTopic?.name) {
        publish(button.selectedTopic.name, String(data.payload));
    }
};

const handleSwitchToggle = (data) => {
    const switchItem = controllerStore.switches.find(s => s.id === data.id);
    if (switchItem?.selectedTopic?.name) {
        publish(switchItem.selectedTopic.name, String(data.payload));
    }
};

const handleSliderChange = (data) => {
    const slider = controllerStore.sliders.find(s => s.id === data.id);
    if (slider?.selectedTopic?.name) {
        publish(slider.selectedTopic.name, String(data.value));
    }
};
</script>