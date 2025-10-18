<template>
    <div class="px-2 pt-2">
        <div class="flex items-center justify-between mb-6">
            <div>
                <div class="text-2xl font-bold flex items-center space-x-3">
                    <span class="text-2xl material-symbols-outlined">
                        drone
                    </span>
                    <p>Drones</p>
                </div>
                <p class="text-gray-600 dark:text-gray-400">Manage your drones and their configurations.</p>
            </div>
            <button @click="showCreateModal = true"
                class="px-4 py-2 text-sm font-medium text-white bg-blue-500 hover:bg-blue-600 rounded-lg shadow-sm transition-colors flex items-center gap-2">
                <span class="text-lg">+</span>
                Add New Drone
            </button>
        </div>
        <hr class="border-0.5 border-gray-200 dark:border-gray-700 mb-6">
        <DroneListComponent :drones="droneStore.drones" @refresh="droneStore.fetchDrones" @edit="handleEditDrone"
            @delete="handleDeleteDrone" @detail="handleDroneDetail" @create="handleCreateDrone" />

        <DroneModalComponent v-if="showCreateModal" :is-open="showCreateModal" :is-edit="false"
            @close="showCreateModal = false" @save="handleCreateDrone" />
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDroneStore } from '@/stores/DroneStore'
import DroneListComponent from '@/components/drones/DroneListComponent.vue'
import DroneModalComponent from '@/components/drones/DroneModalComponent.vue'

const droneStore = useDroneStore()
const showCreateModal = ref(false)

onMounted(async () => {
    await droneStore.fetchDrones()
    await droneStore.fetchMqttClients()
    await droneStore.fetchStreamingClients()
})

const handleCreateDrone = async (droneData) => {
    try {
        await droneStore.createDrone(droneData)
        showCreateModal.value = false
    } catch (err) {
        console.error('Failed to create drone:', err)
    }
}

const handleEditDrone = async (droneId, droneData) => {
    try {
        await droneStore.updateDrone(droneId, droneData)
    } catch (err) {
        console.error('Failed to update drone:', err)
    }
}

const handleDeleteDrone = async (droneId) => {
    try {
        await droneStore.deleteDrone(droneId)
    } catch (err) {
        console.error('Failed to delete drone:', err)
    }
}

const handleDroneDetail = (drone) => {
    console.log('Viewing drone details:', drone)
    // Implement navigation to detail page or show modal
}
</script>