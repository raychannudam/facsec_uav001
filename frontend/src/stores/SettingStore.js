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
    async updateMqttClient(id, data){
      let message = "";
      let status = "";
      await api.put(`/api/v1/mqtt-clients/${id}`, data).then(res=>{
        status = "success";
        message = "Successfully update a MQTT client!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed update this MQTT clients!"
      });
      return {
        status: status,
        message: message
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
        message = err.response?.data?.detail || "Failed to delete this MQTT clients!"
      });
      return {
        status: status,
        message: message
      }
    },
    async createMqttTopic(data){
      data['config'] = {}
      data['status'] = true
      let message = "";
      let status = "";
      await api
          .post("/api/v1/mqtt-topics", data)
          .then((res) => {
          status = "success";
          message = "Successfully created MQTT topic!";
          })
          .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to create MQTT topic!";
          });
      return {
          status: status,
          message: message,
      };
    },
    async getAllMqttTopicByMqttClientId(mqttClientId){
      let message = ""
      let status = ""
      let data = ""
      await api.get(`/api/v1/mqtt-topics?mqtt_client_id=${mqttClientId}`).then((res)=>{
        status = "success";
        message = `Successfully get all MQTT topic for client id ${mqttClientId}!`;
        data = res.data
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || `Failed to get all MQTT topic for client id ${mqttClientId}!`
      });
      return {
        status: status,
        message: message,
        data: data
      }
    }
  },
});