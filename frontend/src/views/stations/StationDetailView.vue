<template>
    <div class="flex flex-col space-y-6" v-if="stationData">
        <!-- Station Details Card -->
        <div
            class="bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-xl p-6 shadow-sm border border-blue-100 dark:border-gray-600">

            <div class="flex items-center space-x-3 mb-4">
                <span class="material-symbols-outlined text-3xl text-blue-600 dark:text-blue-400">warehouse</span>
                <h2 class="text-2xl font-bold text-gray-800 dark:text-white capitalize">{{ stationData.name }}</h2>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
                    <div class="flex items-center space-x-2 text-gray-500 dark:text-gray-400 mb-2">
                        <span class="material-symbols-outlined text-sm">badge</span>
                        <p class="text-xs font-medium uppercase tracking-wide">Station Name</p>
                    </div>
                    <p class="text-lg font-semibold text-gray-900 dark:text-white capitalize">{{ stationData.name }}</p>
                </div>

                <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
                    <div class="flex items-center space-x-2 text-gray-500 dark:text-gray-400 mb-2">
                        <span class="material-symbols-outlined text-sm">description</span>
                        <p class="text-xs font-medium uppercase tracking-wide">Description</p>
                    </div>
                    <p class="text-lg font-semibold text-gray-900 dark:text-white">{{ stationData.description || 'N/A'
                    }}</p>
                </div>

                <div class="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm">
                    <div class="flex items-center space-x-2 text-gray-500 dark:text-gray-400 mb-2">
                        <span class="material-symbols-outlined text-sm">location_on</span>
                        <p class="text-xs font-medium uppercase tracking-wide">Coordinates</p>
                    </div>
                    <p class="text-sm font-mono font-semibold text-gray-900 dark:text-white">
                        {{ stationData.lat.toFixed(6) }}, {{ stationData.long.toFixed(6) }}
                    </p>
                </div>
            </div>
        </div>

        <!-- Assign Drone Card -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center space-x-3">
                    <div class="bg-blue-100 dark:bg-blue-900 p-2 rounded-lg">
                        <span class="material-symbols-outlined text-blue-600 dark:text-blue-400">add_circle</span>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold text-gray-800 dark:text-white">Assign Drone</h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400">Add a drone to this station</p>
                    </div>
                </div>
                <div class="bg-blue-50 dark:bg-blue-900/30 px-4 py-2 rounded-full" v-if="availableDrones.length > 0">
                    <span class="text-sm font-semibold text-blue-600 dark:text-blue-400">
                        {{ availableDrones.length }} available
                    </span>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-12 gap-4 items-end">
                <div class="md:col-span-9">
                    <label for="droneSelect" class="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-2">
                        Select Available Drone
                    </label>
                    <div class="relative">
                        <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
                            <span class="material-symbols-outlined text-gray-400 text-lg">drone</span>
                        </div>
                        <select id="droneSelect" v-model="selectedDroneId"
                            class="pl-10 bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 block w-full p-3 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500 transition-all">
                            <option :value="null" disabled>Choose a drone...</option>
                            <option v-for="drone in availableDrones" :key="drone.id" :value="drone.id">
                                {{ drone.name }} ({{ drone.type }})
                            </option>
                        </select>
                    </div>
                </div>

                <div class="md:col-span-3">
                    <button @click="assignDroneToStation" :disabled="!selectedDroneId || isAssigning"
                        class="w-full px-6 py-3 text-sm font-semibold text-white bg-gradient-to-r from-blue-600 to-blue-700 rounded-lg hover:from-blue-700 hover:to-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:from-blue-500 dark:to-blue-600 dark:hover:from-blue-600 dark:hover:to-blue-700 disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-400 disabled:to-gray-400 flex items-center justify-center space-x-2 transition-all shadow-md hover:shadow-lg">
                        <span class="material-symbols-outlined text-lg" v-if="!isAssigning">add_circle</span>
                        <span class="material-symbols-outlined text-lg animate-spin" v-else>progress_activity</span>
                        <span>{{ isAssigning ? 'Assigning...' : 'Assign Drone' }}</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- Drones List Card -->
        <div class="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-lg border border-gray-200 dark:border-gray-700">
            <div class="flex items-center justify-between mb-6">
                <div class="flex items-center space-x-3">
                    <div class="bg-indigo-100 dark:bg-indigo-900 p-2 rounded-lg">
                        <span class="material-symbols-outlined text-indigo-600 dark:text-indigo-400">drone</span>
                    </div>
                    <div>
                        <h3 class="text-xl font-bold text-gray-800 dark:text-white">Drones in Station</h3>
                        <p class="text-sm text-gray-500 dark:text-gray-400">Manage assigned drones</p>
                    </div>
                </div>
                <div class="flex items-center space-x-2">
                    <span class="text-sm text-gray-600 dark:text-gray-400">Total:</span>
                    <div class="bg-indigo-50 dark:bg-indigo-900/30 px-3 py-1 rounded-full">
                        <span class="text-lg font-bold text-indigo-600 dark:text-indigo-400">
                            {{ stationData.uavs?.length || 0 }}
                        </span>
                    </div>
                </div>
            </div>

            <!-- Drones Table -->
            <div v-if="stationData.uavs && stationData.uavs.length > 0"
                class="relative overflow-x-auto rounded-lg border border-gray-200 dark:border-gray-700">
                <table class="w-full text-sm text-left text-gray-500 dark:text-gray-400">
                    <thead
                        class="text-xs text-gray-700 uppercase bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600 dark:text-gray-300">
                        <tr>
                            <th scope="col" class="px-6 py-4 font-semibold">ID</th>
                            <th scope="col" class="px-6 py-4 font-semibold">Name</th>
                            <th scope="col" class="px-6 py-4 font-semibold">Description</th>
                            <th scope="col" class="px-6 py-4 font-semibold">Status</th>
                            <th scope="col" class="px-6 py-4 font-semibold">Created</th>
                            <th scope="col" class="px-6 py-4 font-semibold">Action</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="drone in stationData.uavs" :key="drone.id"
                            class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 hover:bg-blue-50 dark:hover:bg-gray-700 transition-colors">

                            <td class="px-6 py-4 font-semibold text-gray-900 dark:text-white">
                                #{{ drone.id }}
                            </td>

                            <td class="px-6 py-4 font-medium text-gray-900 dark:text-white">
                                {{ drone.name }}
                            </td>

                            <td class="px-6 py-4 text-gray-700 dark:text-gray-300">
                                {{ drone.description || 'N/A' }}
                            </td>

                            <td class="px-6 py-4">
                                <span class="px-3 py-1.5 text-xs font-semibold rounded-full" :class="{
                                    'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-300': drone.status === 'active',
                                    'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-300': drone.status === 'idle',
                                    'bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-300': drone.status === 'offline',
                                    'bg-gray-200 text-gray-700 dark:bg-gray-700 dark:text-gray-300': !drone.status
                                }">
                                    {{ drone.status || 'Unknown' }}
                                </span>
                            </td>

                            <td class="px-6 py-4 text-xs font-mono text-gray-600 dark:text-gray-400">
                                {{ new Date(drone.created_at).toLocaleString() }}
                            </td>

                            <td class="px-6 py-4">
                                <div>
                                    <button @click="handleRemoveDrone(drone)" :disabled="removingDroneId === drone.id"
                                        class="px-4 py-2 text-xs font-semibold text-white bg-gradient-to-r from-red-500 to-red-600 rounded-lg hover:from-red-600 hover:to-red-700 focus:ring-4 focus:outline-none focus:ring-red-300 dark:from-red-600 dark:to-red-700 dark:hover:from-red-700 dark:hover:to-red-800 disabled:opacity-50 disabled:cursor-not-allowed disabled:from-gray-400 disabled:to-gray-400 flex items-center space-x-1 transition-all shadow-sm hover:shadow-md">
                                        <span class="material-symbols-outlined text-sm"
                                            v-if="removingDroneId !== drone.id">delete</span>
                                        <span class="material-symbols-outlined text-sm animate-spin"
                                            v-else>progress_activity</span>
                                    </button>
                                </div>
                            </td>

                        </tr>
                    </tbody>
                </table>

            </div>

            <!-- Empty State -->
            <div v-else
                class="flex flex-col items-center justify-center p-12 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-lg border-2 border-dashed border-gray-300 dark:border-gray-600">
                <div class="bg-gray-200 dark:bg-gray-600 p-6 rounded-full mb-4">
                    <span class="material-symbols-outlined text-6xl text-gray-400 dark:text-gray-500">
                        drone
                    </span>
                </div>
                <p class="text-lg font-semibold text-gray-700 dark:text-gray-300 text-center mb-2">No drones assigned
                    yet</p>
                <p class="text-sm text-gray-500 dark:text-gray-400 text-center">Use the form above to assign drones to
                    this station</p>
            </div>
        </div>
    </div>

    <!-- Empty State when no station selected -->
    <div class="flex flex-col space-y-6 items-center justify-center w-full p-12 bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-800 dark:to-gray-700 rounded-xl border-2 border-dashed border-gray-300 dark:border-gray-600"
        v-else>
        <div class="bg-gray-200 dark:bg-gray-600 p-8 rounded-full">
            <span class="material-symbols-outlined text-7xl text-gray-400 dark:text-gray-500">
                touch_app
            </span>
        </div>
        <div class="text-center space-y-2">
            <p class="text-xl font-semibold text-gray-700 dark:text-gray-300">Select a Station</p>
            <p class="text-sm text-gray-500 dark:text-gray-400 italic">Click on a station icon on the map to view
                details</p>
        </div>
    </div>

    <!-- Remove Drone Modal -->
    <DeleteModal :is-open="showRemoveModal" title="Remove Drone"
        :message="`Are you sure you want to remove '${droneToRemove?.name}' from this station?`" confirm-text="Remove"
        :item-id="droneToRemove?.id" @close="showRemoveModal = false" @confirm="confirmRemoveDrone" />
</template>

<script setup>
import { ref, watch, onMounted } from 'vue';
import { useStationStore } from '@/stores/StationStore';
import { useAppStore } from '@/stores/AppStore';
import DeleteModal from '@/components/utils/DeleteModal.vue';

const props = defineProps({
    stationData: {
        type: Object,
        default: null
    }
});

const emit = defineEmits(['onDroneAssigned', 'onDroneRemoved']);

const stationStore = useStationStore();
const appStore = useAppStore();

const availableDrones = ref([]);
const selectedDroneId = ref(null);
const isAssigning = ref(false);
const removingDroneId = ref(null);
const showRemoveModal = ref(false);
const droneToRemove = ref(null);

// Fetch available drones
const fetchAvailableDrones = async () => {
    const res = await stationStore.getAvailableUavs();
    if (res.status === 'success') {
        availableDrones.value = res.data;
    }
};

// Assign drone to station
const assignDroneToStation = async () => {
    if (!selectedDroneId.value || !props.stationData) return;

    isAssigning.value = true;
    const res = await stationStore.assignUavToStation(props.stationData.id, selectedDroneId.value);
    isAssigning.value = false;

    appStore.displayRightToast(res.status, res.message);

    if (res.status === 'success') {
        selectedDroneId.value = null;
        await fetchAvailableDrones();
        emit('onDroneAssigned');
    }
};

// Handle remove drone button click
const handleRemoveDrone = (drone) => {
    droneToRemove.value = drone;
    showRemoveModal.value = true;
};

// Confirm remove drone from station
const confirmRemoveDrone = async (droneId) => {
    showRemoveModal.value = false;
    removingDroneId.value = droneId;
    const res = await stationStore.removeUavFromStation(droneId);
    removingDroneId.value = null;

    appStore.displayRightToast(res.status, res.message);

    if (res.status === 'success') {
        await fetchAvailableDrones();
        emit('onDroneRemoved');
    }
};

// Watch for station changes
watch(() => props.stationData, (newStation) => {
    if (newStation) {
        fetchAvailableDrones();
    }
}, { immediate: true });

onMounted(() => {
    fetchAvailableDrones();
});
</script>