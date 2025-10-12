import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '@/plugins/api'

export const useDroneStore = defineStore('drone', () => {
  const drones = ref([])
  const mqttClients = ref([])
  const streamingClients = ref([])
  const loading = ref(false)
  const error = ref(null)

  const droneTypes = [
    'Multi-roter',
    'Fixed-wing',
    'Single-roter',
    'Hybrid VTOL'
  ]

  const fetchDrones = async () => {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get('/api/v1/uavs')
      drones.value = data
    } catch (err) {
      error.value = err.response?.data?.message || err.message
      console.error('Error fetching drones:', err)
    } finally {
      loading.value = false
    }
  }

  const fetchMqttClients = async () => {
    try {
      const { data } = await api.get('/api/v1/mqtt-clients')
      mqttClients.value = data
    } catch (err) {
      console.error('Error fetching mqtt clients:', err)
    }
  }

  const fetchStreamingClients = async () => {
    try {
      const { data } = await api.get('/api/v1/streaming-clients')
      streamingClients.value = data
    } catch (err) {
      console.error('Error fetching streaming clients:', err)
    }
  }

  const createDrone = async (droneData) => {
    try {
      const { data: newDrone } = await api.post('/api/v1/uavs', droneData)
      drones.value.push(newDrone)
      return newDrone
    } catch (err) {
      console.error('Error creating drone:', err)
      throw err
    }
  }

  const updateDrone = async (id, droneData) => {
    try {
      const { data: updatedDrone } = await api.put(`/api/v1/uavs/${id}`, droneData)
      const index = drones.value.findIndex(d => d.id === id)
      if (index !== -1) drones.value[index] = updatedDrone
      return updatedDrone
    } catch (err) {
      console.error('Error updating drone:', err)
      throw err
    }
  }

  const deleteDrone = async (id) => {
    try {
      await api.delete(`/api/v1/uavs/${id}`)
      drones.value = drones.value.filter(d => d.id !== id)
    } catch (err) {
      console.error('Error deleting drone:', err)
      throw err
    }
  }

  return {
    drones,
    mqttClients,
    streamingClients,
    droneTypes,
    loading,
    error,
    fetchDrones,
    fetchMqttClients,
    fetchStreamingClients,
    createDrone,
    updateDrone,
    deleteDrone
  }
})
