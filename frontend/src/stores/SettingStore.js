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
    },
    async deleteMqttTopic(id){
      let message = ""
      let status = ""
      await api.delete(`/api/v1/mqtt-topics/${id}`).then(res=>{
        status = "success";
        message = "Successfully delete a MQTT topic!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to delete this MQTT topic!"
      });
      return {
        status: status,
        message: message
      }
    },
    async getAllStreamingClients(){
      let message = ""
      let status = ""
      let data = ""
      await api.get("/api/v1/streaming-clients").then((res)=>{
        status = "success";
        message = "Successfully get all streaming clients!";
        data = res.data
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to get all streaming clients!"
      });
      return {
        status: status,
        message: message,
        data: data
      }
    },
    async createStreamingClient(data){
      data['config'] = {"actions": ["read", "publish"]}
      data['status'] = true
      let message = "";
      let status = "";
      await api
          .post("/api/v1/streaming-clients", data)
          .then((res) => {
          status = "success";
          message = "Successfully created streaming client!";
          })
          .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to create streaming client!";
          });
      return {
          status: status,
          message: message,
      };
    },
    async deleteStreamingClient(id){
      let message = ""
      let status = ""
      await api.delete(`/api/v1/streaming-clients/${id}`).then(res=>{
        status = "success";
        message = "Successfully delete a streaming client!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to delete this streaming client!"
      });
      return {
        status: status,
        message: message
      }
    },
    async updateStreamingClient(id, data){
      let message = "";
      let status = "";
      await api.put(`/api/v1/streaming-clients/${id}`, data).then(res=>{
        status = "success";
        message = "Successfully update a streaming client!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed update this streaming clients!"
      });
      return {
        status: status,
        message: message
      }
    },
    async requestValidationCode(id){
      let message = "";
      let status = "";
      await api.get(`/api/v1/streaming-clients/${id}/request-validation-code`).then(res=>{
        status = "success";
        message = "Reset code was sent to your email! Pleae check your inbox.";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to send reset password code to your email!"
      });
      return {
        status: status,
        message: message
      }
    },
    async updateStreamingClientPassword(id, data){
      let message = "";
      let status = "";
      await api.put(`/api/v1/streaming-clients/${id}/update-password?validation_code=${data.validation_code}&new_password=${data.new_password}`, data).then(res=>{
        status = "success";
        message = "Successfully update the password!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to to update the password!"
      });
      return {
        status: status,
        message: message
      }
    },
    async crateStreamingUrl(data){
      let status = ""
      let message = ""
      data['config'] = {"protocols":["rstp", "webrtc"]}
      data['status'] = true
      await api.post("/api/v1/streaming-urls", data).then((res) => {
          status = "success";
          message = "Successfully created streaming URL!";
          })
          .catch((err) => {
          status = "fail";
          message = err.response?.data?.detail || "Failed to create streaming URL!";
          });
      return {
          status: status,
          message: message,
      };
    },
    async getAllStreamingUrls(streamingClientId){
      let status = ""
      let message = ""
      let data = {}
      await api.get(`/api/v1/streaming-urls/${streamingClientId}`).then((res)=>{
        status = "success";
        message = "Successfully get all streaming URLs!";
        data = res.data
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to get all streaming URLs!"
      });
      return {
        status: status,
        message: message,
        data: data
      }
    },
    async deleteStreamingUrl(id){
      let message = ""
      let status = ""
      await api.delete(`/api/v1/streaming-urls/${id}`).then(res=>{
        status = "success";
        message = "Successfully delete a streaming URL!";
      }).catch(err=>{
        status = "fail";
        message = err.response?.data?.detail || "Failed to delete this streaming URL!"
      });
      return {
        status: status,
        message: message
      }
    },
  },
});