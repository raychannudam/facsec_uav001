import { defineStore } from "pinia";
import api from "@/plugins/api";

export const useUavStore = defineStore("uav", {
    state(){
        return{

        }
    },
    actions:{
        async getAllUavs(query=""){
            let status = ""
            let message = ""
            let data = undefined
            await api.get(`/api/v1/uavs?query=${query}`).then((res)=>{
                status = "success";
                message = "Successfully get all UAVs!";
                data = res.data
            }).catch(err=>{
                status = "fail";
                message = err.response?.data?.detail || "Failed to get all UAVs!"
            });
            return {
                status: status,
                message: message,
                data: data
            }
        }
    }
})