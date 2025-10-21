import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/plugins/api";
import { useAppStore } from "@/stores/AppStore"; // Import AppStore

export const useDroneStore = defineStore("drone", () => {
  const appStore = useAppStore(); // Initialize AppStore
  
  const drones = ref([]);
  const mqttClients = ref([]);
  const streamingClients = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const droneTypes = [
    "Multi-roter",
    "Fixed-wing",
    "Single-roter",
    "Hybrid VTOL",
  ];

  const fetchDrones = async () => {
    appStore.displayPageLoading(true);
    loading.value = true;
    error.value = null;
    
    let status = "fail";
    let message = "";
    
    try {
      const { data } = await api.get("/api/v1/uavs");
      status = "success";
      message = "Successfully getting all drones!";
      drones.value = data;
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to get all drones!";
      error.value = message;
      console.error("Error fetching drones:", err);
    } finally {
      loading.value = false;
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

  const fetchMqttClients = async () => {
    appStore.displayPageLoading(true);
    
    let status = "fail";
    let message = "";
    
    try {
      const { data } = await api.get("/api/v1/mqtt-clients");
      mqttClients.value = data;
      status = "success";
      message = "MQTT clients loaded successfully!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to fetch MQTT clients!";
      console.error("Error fetching mqtt clients:", err);
    } finally {
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

  const fetchStreamingClients = async () => {
    appStore.displayPageLoading(true);
    
    let status = "fail";
    let message = "";
    
    try {
      const { data } = await api.get("/api/v1/streaming-clients");
      streamingClients.value = data;
      status = "success";
      message = "Streaming clients loaded successfully!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to fetch streaming clients!";
      console.error("Error fetching streaming clients:", err);
    } finally {
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

  const createDrone = async (droneData) => {
    appStore.displayPageLoading(true);
    
    let status = "fail";
    let message = "";
    
    try {
      const { data: newDrone } = await api.post("/api/v1/uavs", droneData);
      drones.value.push(newDrone);
      status = "success";
      message = "Drone created successfully!";
      return newDrone;
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create drone!";
      console.error("Error creating drone:", err);
      throw err;
    } finally {
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

  const updateDrone = async (id, droneData) => {
    appStore.displayPageLoading(true);
    
    let status = "fail";
    let message = "";
    
    try {
      const { data: updatedDrone } = await api.put(
        `/api/v1/uavs/${id}`,
        droneData
      );
      const index = drones.value.findIndex((d) => d.id === id);
      if (index !== -1) drones.value[index] = updatedDrone;
      status = "success";
      message = "Drone updated successfully!";
      return updatedDrone;
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to update drone!";
      console.error("Error updating drone:", err);
      throw err;
    } finally {
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

  const deleteDrone = async (id) => {
    appStore.displayPageLoading(true);
    
    let status = "fail";
    let message = "";
    
    try {
      await api.delete(`/api/v1/uavs/${id}`);
      drones.value = drones.value.filter((d) => d.id !== id);
      status = "success";
      message = "Drone deleted successfully!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to delete drone!";
      console.error("Error deleting drone:", err);
      throw err;
    } finally {
      appStore.displayPageLoading(false);
      appStore.displayRightToast(status, message);
    }
  };

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
    deleteDrone,
  };
});