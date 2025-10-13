<template>
    <div class="container mx-auto px-4 py-8">
        <h1 class="text-3xl font-bold mb-8">Drones</h1>

        <DroneListComponent :drones="droneStore.drones" :loading="droneStore.loading" @refresh="droneStore.fetchDrones"
            @edit="handleEditDrone" @delete="handleDeleteDrone" @detail="handleDroneDetail"
            @create="handleCreateDrone" />
    </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useDroneStore } from '@/stores/droneStore'
import DroneListComponent from '@/components/drones/DroneListComponent.vue'

const droneStore = useDroneStore()

onMounted(async () => {
    await droneStore.fetchDrones()
    await droneStore.fetchMqttClients()
    await droneStore.fetchStreamingClients()
})

const handleCreateDrone = async (droneData) => {
    try {
        await droneStore.createDrone(droneData)
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
    if (confirm('Are you sure you want to delete this drone?')) {
        try {
            await droneStore.deleteDrone(droneId)
        } catch (err) {
            console.error('Failed to delete drone:', err)
        }
    }
}

const handleDroneDetail = (drone) => {
    console.log('Viewing drone details:', drone)
    // Implement navigation to detail page or show modal
}
</script>