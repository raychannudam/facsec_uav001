import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/plugins/api";
import { useAppStore } from "./AppStore";

export const useControllerStore = defineStore("controller", () => {
  const appStore = useAppStore();

  const controllers = ref([]);
  const selectedController = ref(null);

  const hasSelectedTopic = (item) =>
    item.selectedTopic && Object.keys(item.selectedTopic).length > 0;

  const buttons = computed(() => {
    if (!selectedController.value?.config?.mqttTopics) return [];
    return selectedController.value.config.mqttTopics.filter(
      (item) => item.type === "button" && hasSelectedTopic(item)
    );
  });

  const switches = computed(() => {
    if (!selectedController.value?.config?.mqttTopics) return [];
    return selectedController.value.config.mqttTopics.filter(
      (item) => item.type === "switch" && hasSelectedTopic(item)
    );
  });

  const sliders = computed(() => {
    if (!selectedController.value?.config?.mqttTopics) return [];
    return selectedController.value.config.mqttTopics.filter(
      (item) => item.type === "slider" && hasSelectedTopic(item)
    );
  });

  const getAllControllers = async () => {
    let status = "fail";
    let message = "";
    let data = undefined;
    try {
      const response = await api.get("/api/v1/controllers");
      controllers.value = response.data;
      data = response.data;
      if (response.data.length > 0 && !selectedController.value) {
        selectedController.value = response.data[0];
      }
      status = "success";
      message = "Successfully got all controllers!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to get all controllers!";
      console.error("Error fetching controllers:", err);
    }
    return { status, message, data };
  };

  const createController = async (data) => {
    let status = "fail";
    let message = "";
    let createdData = undefined;
    try {
      const response = await api.post("/api/v1/controllers", data);
      controllers.value.push(response.data);
      createdData = response.data;
      status = "success";
      message = "Successfully created a new profile!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create a new profile!";
      console.error("Error creating controller:", err);
    }
    return { status, message, data: createdData };
  };

  const updateController = async (id, data) => {
    let status = "fail";
    let message = "";
    try {
      await api.put(`/api/v1/controllers/${id}`, data);
      const index = controllers.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        controllers.value[index] = { ...controllers.value[index], ...data };
      }
      if (selectedController.value?.id === id) {
        selectedController.value = { ...selectedController.value, ...data };
      }
      status = "success";
      message = "Successfully updated your profile!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to update your profile!";
      console.error("Error updating controller:", err);
    }
    return { status, message };
  };

  const deleteController = async (id) => {
    let status = "fail";
    let message = "";
    try {
      await api.delete(`/api/v1/controllers/${id}`);
      const index = controllers.value.findIndex((c) => c.id === id);
      if (index !== -1) {
        controllers.value.splice(index, 1);
      }
      if (selectedController.value?.id === id) {
        selectedController.value =
          controllers.value.length > 0 ? controllers.value[0] : null;
      }
      status = "success";
      message = "Successfully deleted the profile!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to delete the profile!";
      console.error("Error deleting controller:", err);
    }
    return { status, message };
  };

  const selectController = (controller) => {
    selectedController.value = controller;
  };

  return {
    // State
    controllers,
    selectedController,

    // Computed
    buttons,
    switches,
    sliders,

    // Actions
    getAllControllers,
    createController,
    updateController,
    deleteController,
    selectController,
  };
});
