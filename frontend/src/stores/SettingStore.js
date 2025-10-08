import { defineStore } from "pinia";
import api from "@/plugins/api";
export const useSettingStore = defineStore("setting", {
  state: () => {
    return {
     
    };
  },
  actions: {
    async createMqttClient(data) {
        data['user_id'] = Number(localStorage.getItem("current_user_id"))
        data['config'] = {}
        data['status'] = true
        let message = "";
        let status = "";
        await api
            .post("/api/v1/mqtt-clients", data)
            .then((res) => {
            status = "success";
            message = "Successfully created MQTT client!";
            })
            .catch((err) => {
            status = "fail";
            message = err.response?.data?.detail || "Failed to create MQTT client!";
            });
        return {
            status: status,
            message: message,
        };
    },
    async getAllMqttClients(){
      let message = ""
      let status = ""
      let data = ""
      await api.get("/api/v1/mqtt-clients").then((res)=>{
        status = "success";
        message = "Successfully get all MQTT clients!";
        data = res.data
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to get all MQTT clients!"
      });
      return {
        status: status,
        message: message,
        data: data
      }
    },
    async deleteMqttClient(id){
      let message = ""
      let status = ""
      await api.delete(`/api/v1/mqtt-clients/${id}`).then(res=>{
        status = "success";
        message = "Successfully delete a MQTT client!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to get all MQTT clients!"
      });
      return {
        status: status,
        message: message
      }
    }
  },
});