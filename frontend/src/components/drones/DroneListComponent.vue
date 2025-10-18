<template>
    <div>
        <!-- Drone Grid -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-5">
            <div v-for="drone in drones" :key="drone.id"
                class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-xl transition-shadow">
                <div
                    class="w-full h-40 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center overflow-hidden">
                    <img v-if="drone.image" :src="drone.image" :alt="drone.name" class="w-full h-full object-cover" />
                    <div v-else class="text-white text-4xl">🚁</div>
                </div>

                <div class="p-4">
                    <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-3 truncate">
                        {{ drone.name }}
                    </h3>

                    <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1.5 mb-4">
                        <p>
                            <span class="font-semibold">Type: </span>
                            <span class="text-gray-900 dark:text-gray-300">{{ drone.type }}</span>
                        </p>
                        <p>
                            <span class="font-semibold">MQTT: </span>
                            <span class="text-gray-900 dark:text-gray-300">{{ drone.mqtt_client.name }}</span>
                        </p>
                        <p>
                            <span class="font-semibold">Streaming: </span>
                            <span class="text-gray-900 dark:text-gray-300">{{ drone.streaming_client.name }}</span>
                        </p>
                    </div>

                    <div class="flex gap-2">
                        <button
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-blue-500 hover:bg-blue-600 rounded transition-colors">
                            Detail
                        </button>
                        <button @click="openEditModal(drone)"
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-green-500 hover:bg-green-600 rounded transition-colors">
                            Edit
                        </button>
                        <button @click="handleDeleteDrone(drone)"
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-red-500 hover:bg-red-600 rounded transition-colors">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Empty State -->
        <div v-if="!drones || drones.length === 0" class="text-center py-12 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div class="text-5xl mb-4">🚁</div>
            <p class="text-gray-600 dark:text-gray-400 mb-4">No drones available</p>
            <button @click="showCreateModal = true"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-lg transition-colors">
                Add Your First Drone
            </button>
        </div>

        <DroneModalComponent :is-open="showCreateModal || showEditModal" :is-edit="showEditModal" :drone="editingDrone"
            @close="closeModal" @save="handleSave" />

        <DroneDeleteComponent :is-open="showDeleteModal"
            :message="'Are you sure you want to delete this drone? This will permanently remove all associated data.'"
            :drone="droneToDelete" @close="showDeleteModal = false" @confirm="confirmDelete" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import DroneModalComponent from './DroneModalComponent.vue'
import DroneDeleteComponent from './DroneDeleteComponent.vue'

defineProps({
    drones: {
        type: Array,
        default: () => []
    }
})

const emit = defineEmits(['refresh', 'edit', 'delete', 'detail', 'create'])

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingDrone = ref(null)
const showDeleteModal = ref(false)
const droneToDelete = ref(null)

const openEditModal = (drone) => {
    editingDrone.value = { ...drone }
    showEditModal.value = true
}

const closeModal = () => {
    showCreateModal.value = false
    showEditModal.value = false
    showDeleteModal.value = false
    editingDrone.value = null
}

const handleSave = (droneData) => {
    if (showEditModal.value) emit('edit', editingDrone.value.id, droneData)
    else emit('create', droneData)
    closeModal()
}

const handleDeleteDrone = (drone) => {
    droneToDelete.value = drone
    showDeleteModal.value = true
}

const confirmDelete = async (droneId) => {
    emit('delete', droneId)
    closeModal()
}
</script>