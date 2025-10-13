<template>
    <div>
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-4">
            <div v-for="drone in drones" :key="drone.id"
                class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
                <div
                    class="w-full h-40 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center overflow-hidden">
                    <img v-if="drone.image" :src="drone.image" :alt="drone.name" class="w-full h-full object-cover" />
                    <div v-else class="text-white text-4xl">🚁</div>
                </div>

                <div class="p-4">
                    <h3 class="font-bold text-lg text-gray-900 dark:text-white mb-2 truncate">
                        {{ drone.name }}
                    </h3>

                    <div class="text-sm text-gray-600 dark:text-gray-400 space-y-1 mb-4">
                        <p><span class="font-semibold">Type:</span> {{ drone.type }}</p>
                        <p><span class="font-semibold">MQTT:</span> {{ drone.mqtt_client_name }}</p>
                        <p><span class="font-semibold">Streaming:</span> {{ drone.streaming_client_name }}</p>
                    </div>

                    <div class="flex gap-2">
                        <button @click="$emit('detail', drone)"
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-blue-500 hover:bg-blue-600 rounded transition-colors">
                            Detail
                        </button>
                        <button @click="openEditModal(drone)"
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-green-500 hover:bg-green-600 rounded transition-colors">
                            Edit
                        </button>
                        <button @click="$emit('delete', drone.id)"
                            class="flex-1 px-3 py-2 text-xs font-medium text-white bg-red-500 hover:bg-red-600 rounded transition-colors">
                            Delete
                        </button>
                    </div>
                </div>
            </div>

            <div @click="showCreateModal = true"
                class="bg-white dark:bg-gray-800 rounded-lg shadow-md overflow-hidden cursor-pointer hover:shadow-lg transition-all border-2 border-dashed border-gray-300 dark:border-gray-600 hover:border-blue-500 dark:hover:border-blue-400 flex items-center justify-center min-h-[320px]">
                <div class="text-center">
                    <div class="text-5xl text-gray-400 dark:text-gray-500 mb-2">+</div>
                    <p class="text-gray-600 dark:text-gray-400">Add New Drone</p>
                </div>
            </div>
        </div>

        <DroneModalComponent v-if="showCreateModal || showEditModal" :is-open="showCreateModal || showEditModal"
            :is-edit="showEditModal" :drone="editingDrone" @close="closeModal" @save="handleSave" />
    </div>
</template>

<script setup>
import { ref } from 'vue'
import DroneModalComponent from './DroneModalComponent.vue'

defineProps({
    drones: {
        type: Array,
        default: () => []
    },
    loading: {
        type: Boolean,
        default: false
    }
})

const emit = defineEmits(['refresh', 'edit', 'delete', 'detail', 'create'])

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingDrone = ref(null)

const openEditModal = (drone) => {
    editingDrone.value = { ...drone }
    showEditModal.value = true
}

const closeModal = () => {
    showCreateModal.value = false
    showEditModal.value = false
    editingDrone.value = null
}

const handleSave = (droneData) => {
    if (showEditModal.value) emit('edit', editingDrone.value.id, droneData)
    else emit('create', droneData)
    closeModal()
}
</script>