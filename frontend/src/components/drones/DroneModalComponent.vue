<template>
    <div v-if="isOpen" class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
        <div
            class="bg-white dark:bg-gray-800 rounded-lg shadow-lg max-w-2xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div
                class="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4 flex justify-between items-center flex-shrink-0">
                <div>
                    <p class="text-xs text-gray-600 dark:text-gray-400" v-if="isEdit">
                        Editing Drone
                    </p>
                    <h2 class="text-xl font-bold text-gray-900 dark:text-white">
                        {{ isEdit ? (formData.name || 'Untitled') : 'Creating New Drone' }}
                    </h2>
                </div>
                <button @click="closeModal"
                    class="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="M6 18L18 6M6 6l12 12" />
                    </svg>
                </button>
            </div>

            <form @submit.prevent="handleSubmit" class="p-6 space-y-3 overflow-y-auto flex-1">
                <div class="relative">
                    <input v-model="formData.name" type="text" id="droneName"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " required />
                    <label for="droneName"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        Drone Name *
                    </label>
                </div>

                <div class="relative">
                    <select v-model="formData.type" id="droneType"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        required>
                        <option value="">Select a type</option>
                        <option v-for="type in droneTypes" :key="type" :value="type">
                            {{ type }}
                        </option>
                    </select>
                    <label for="droneType"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        Drone Type *
                    </label>
                </div>

                <div class="relative">
                    <select v-model="formData.mqtt_client_id" id="mqttClient"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        required>
                        <option value="">Select MQTT Client</option>
                        <option v-for="client in mqttClients" :key="client.id" :value="client.id">
                            {{ client.name }}
                        </option>
                    </select>
                    <label for="mqttClient"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        MQTT Client *
                    </label>
                </div>

                <div class="relative">
                    <select v-model="formData.streaming_client_id" id="streamingClient"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        required>
                        <option value="">Select Streaming Client</option>
                        <option v-for="client in streamingClients" :key="client.id" :value="client.id">
                            {{ client.name }}
                        </option>
                    </select>
                    <label for="streamingClient"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        Streaming Client *
                    </label>
                </div>

                <div class="relative">
                    <input v-model="formData.last_lat" type="number" id="latitude" step="0.000001"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " required />
                    <label for="latitude"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        Latitude *
                    </label>
                </div>

                <div class="relative">
                    <input v-model="formData.last_long" type="number" id="longitude" step="0.000001"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " required />
                    <label for="longitude"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">
                        Longitude *
                    </label>
                </div>

                <div class="relative">
                    <JsonEditorVue v-model="formData.operation_data" mode="text"></JsonEditorVue>
                </div>

                <div class="flex gap-3 pt-4">
                    <button type="submit"
                        class="flex-1 px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                        {{ isEdit ? 'Update Drone' : 'Create Drone' }}
                    </button>
                    <button type="button" @click="closeModal"
                        class="flex-1 px-5 py-3 text-base font-medium text-center text-white bg-red-700 rounded-lg hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">
                        Cancel
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import JsonEditorVue from "json-editor-vue"
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'
import { useDroneStore } from '@/stores/droneStore'

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    isEdit: {
        type: Boolean,
        default: false
    },
    drone: {
        type: Object,
        default: null
    }
})

const mqttClients = ref([])
const streamingClients = ref([])

const emit = defineEmits(['close', 'save'])
const droneStore = useDroneStore()

onMounted(() => {
    mqttClients.value = droneStore.mqttClients;
    streamingClients.value = droneStore.streamingClients;
})

const formData = ref({
    name: '',
    type: '',
    mqtt_client_id: '',
    streaming_client_id: '',
    last_lat: '',
    last_long: '',
    operation_data: {}
})

const droneTypes = ref([
    'Multi-roter',
    'Fixed-wing',
    'Single-roter',
    'Hybrid VTOL'
])

const resetForm = () => {
    formData.value = {
        name: '',
        type: '',
        mqtt_client_id: '',
        streaming_client_id: '',
        last_lat: '',
        last_long: '',
        operation_data: {}
    }
}

watch(() => props.drone, (newDrone) => {
    if (newDrone) {
        formData.value = {
            name: newDrone.name || '',
            type: newDrone.type || '',
            mqtt_client_id: newDrone.mqtt_client_id || '',
            streaming_client_id: newDrone.streaming_client_id || '',
            last_lat: newDrone.last_lat || '',
            last_long: newDrone.last_long || '',
            operation_data: newDrone.operation_data || {}
        }
    } else {
        resetForm()
    }
}, { immediate: true })

const handleSubmit = () => {
    try {
        const parsedData = {
            ...formData.value,
            operation_data: typeof formData.value.operation_data === 'string'
                ? JSON.parse(formData.value.operation_data)
                : JSON.parse(JSON.stringify(formData.value.operation_data))
        }
        emit('save', parsedData)
        closeModal()
    } catch (err) {
        console.error('JSON parse error:', err)
        alert('Invalid JSON in Operation Data field')
    }
}

const closeModal = () => {
    resetForm()
    emit('close')
}
</script>