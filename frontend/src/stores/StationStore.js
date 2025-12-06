import { defineStore } from "pinia";
import api from "@/plugins/api";

export const useStationStore = defineStore("station", {
  state() {
    return {};
  },
  actions: {
    async createStation(data) {
      let status = "";
      let message = "";
      await api
        .post("/api/v1/stations", data)
        .then((res) => {
          status = "success";
          message = "Successfully created station!";
        })
        .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to create station!";
        });
      return {
        status: status,
        message: message,
      };
    },
    async getAllStations(query = "") {
      let status = "";
      let message = "";
      let data = [];
      await api
        .get(`/api/v1/stations?query=${query}`)
        .then((res) => {
          status = "success";
          message = "Successfully getting all stations!";
          data = res.data;
        })
        .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to get all stations!";
        });
      return {
        status: status,
        message: message,
        data: data,
      };
    },
    async deleteStation(stationId) {
      let status = "";
      let message = "";
      await api
        .delete(`/api/v1/stations/${stationId}`)
        .then((res) => {
          status = "success";
          message = "Successfully deleted station!";
        })
        .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to delete station!";
        });
      return {
        status: status,
        message: message,
      };
    },
    async getAvailableUavs() {
      let status = "";
      let message = "";
      let data = [];
      await api
        .get("/api/v1/avaliable-uavs")
        .then((res) => {
          status = "success";
          message = "Successfully getting available UAVs!";
          data = res.data;
        })
        .catch((err) => {
          status = "fail";
          message =
            err.response?.data?.detail || "Failed to get available UAVs!";
        });
      return {
        status: status,
        message: message,
        data: data,
      };
    },
    async assignUavToStation(stationId, uavId) {
      let status = "";
      let message = "";
      console.log("stationId", stationId);
      console.log("uavId", uavId);
      await api
        .put(`/api/v1/uavs/${uavId}`, { station_id: stationId })
        .then((res) => {
          status = "success";
          message = "Successfully assigned UAV to station!";
        })
        .catch((err) => {
          status = "fail";
          message =
            err.response?.data?.detail || "Failed to assign UAV to station!";
        });

      return {
        status: status,
        message: message,
      };
    },
    async removeUavFromStation(uavId) {
      let status = "";
      let message = "";
      console.log("Removing UAV ID:", uavId);
      await api
        .put(`/api/v1/uavs/${uavId}`, { station_id: null })
        .then((res) => {
          status = "success";
          message = "Successfully removed UAV from station!";
        })
        .catch((err) => {
          status = "fail";
          message =
            err.response?.data?.detail || "Failed to remove UAV from station!";
        });

      return {
        status: status,
        message: message,
      };
    },
  },
});
