import { defineStore } from "pinia";
import api from "@/plugins/api";

export const useStationStore = defineStore("station", {
    state(){
        return {

        }
    },
    actions:{
        async createStation(data){
            let status = ""
            let message = ""
            await api.post("/api/v1/stations", data).then((res) => {
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
        async getAllStations(query=""){
            let status = ""
            let message = ""
            let data = []
            await api.get(`/api/v1/stations?query=${query}`).then((res) => {
                status = "success";
                message = "Successfully getting all stations!";
                data = res.data
            })
            .catch((err) => {
                status = "fail";
                message = err.response?.data?.detail || "Failed to get all stations!";
            });
            return {
                status: status,
                message: message,
                data: data
            };
        }
    }
})