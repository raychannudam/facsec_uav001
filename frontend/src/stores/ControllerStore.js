import { defineStore } from "pinia";
import { ref, computed } from "vue";
import api from "@/plugins/api";
import { useAppStore } from "./AppStore";

export const useControllerStore = defineStore("controller", () => {
    const appStore = useAppStore();

    const controllers = ref([]);
    const selectedController = ref(null);

    const buttons = computed(() => {
        if (!selectedController.value?.config?.mqttTopics) return [];
        return selectedController.value.config.mqttTopics.filter(item => item.type === 'button');
    });

    const switches = computed(() => {
        if (!selectedController.value?.config?.mqttTopics) return [];
        return selectedController.value.config.mqttTopics.filter(item => item.type === 'switch');
    });

    const sliders = computed(() => {
        if (!selectedController.value?.config?.mqttTopics) return [];
        return selectedController.value.config.mqttTopics.filter(item => item.type === 'slider');
    });

    const getAllControllers = async () => {
        appStore.displayPageLoading(true);
        let status = "fail";
        let message = "";
        let data = undefined;
        try {
            const response = await api.get("/api/v1/controllers/");
            controllers.value = response.data;
            data = response.data;
            if (response.data.length > 0 && !selectedController.value) {
                selectedController.value = response.data[0];
            }
            status = "success";
            message = "Successfully get all controllers!";
        } catch (err) {
            status = "fail";
            message = err.response?.data?.detail || "Failed to get all controllers!";
            console.error("Error fetching controllers:", err);
        } finally {
            appStore.displayPageLoading(false);
            appStore.displayRightToast(status, message);
        }
        return {
            status: status,
            message: message,
            data: data
        };
    };

    const updateController = async (id, data) => {
        appStore.displayPageLoading(true);
        let status = "fail";
        let message = "";
        try {
            await api.put(`/api/v1/controllers/${id}`, data);
            const index = controllers.value.findIndex(c => c.id === id);
            if (index !== -1) {
                controllers.value[index] = { ...controllers.value[index], ...data };
            }
            if (selectedController.value?.id === id) {
                selectedController.value = { ...selectedController.value, ...data };
            }
            status = "success";
            message = "Successfully update your controller!";
        } catch (err) {
            status = "fail";
            message = err.response?.data?.detail || "Failed to update your controller!";
            console.error("Error updating controller:", err);
        } finally {
            appStore.displayPageLoading(false);
            appStore.displayRightToast(status, message);
        }
        return {
            status: status,
            message: message
        };
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
        updateController,
        selectController
    };
});