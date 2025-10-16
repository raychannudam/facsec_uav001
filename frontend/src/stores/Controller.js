import { defineStore } from "pinia";
import api from "@/plugins/api";

export const useControllerStore = defineStore("controller", {
    state(){
        return{

        }
    },
    actions:{
        async getAllControllers(){
            let status = ""
            let message = ""
            let data = undefined
            await api.get("/api/v1/controllers").then((res)=>{
                status = "success";
                message = "Successfully get all controllers!";
                data = res.data
            }).catch(err=>{
                status = "fail";
                message = err.response?.data?.detail || "Failed to get all controllers!"
            });
            return {
                status: status,
                message: message,
                data: data
            }
        },
        async updateController(id, data){
            let status = ""
            let message = ""
            await api.put(`/api/v1/controllers/${id}`, data).then((res)=>{
                status = "success";
                message = "Successfully update your controller!";
            }).catch(err=>{
                status = "fail";
                message = err.response?.data?.detail || "Failed to update your controller!"
            });
            return {
                status: status,
                message: message
            }
        }
    }
})