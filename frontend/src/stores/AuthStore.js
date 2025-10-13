import { defineStore } from "pinia"
import api from "@/plugins/api"

export const useAuthStore = defineStore("auth", {
  state: () => {
    return {
      api_url: process.env.VUE_APP_API_URL,
      current_user: undefined,
    }
  },
  actions: {
    async signin(username, password) {
      let formData = new FormData()
      let message = ""
      let status = ""
      formData.append("grant_type", "password")
      formData.append("username", username)
      formData.append("password", password)
      await api
        .post("/api/v1/token", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
            skipAuth: true, // <-- tells interceptor to NOT add Authorization header
          },
        })
        .then((res) => {
          localStorage.setItem("access_token", res.data.access_token)
          localStorage.setItem("refresh_token", res.data.refresh_token)
          status = "success"
          message = "Successfully signed in!"
        })
        .catch((err) => {
          status = "fail"
          message = err.response?.data?.detail || "Sign-in failed"
        })
      return {
        status: status,
        message: message,
      }
    },
    async getProfile() {
      let message = ""
      let status = ""
      await api
        .get("/api/v1/users/me")
        .then((res) => {
          this.current_user = res.data
          localStorage.setItem("current_user_id", res.data.id)
          status = "success"
          message = "Successfully fetched profile!"
        })
        .catch((err) => {
          status = "fail"
          message = err.response?.data?.detail || "Failed to fetch profile"
        })
      return {
        status: status,
        message: message,
      }
    },
    signout() {
      localStorage.removeItem("access_token")
      localStorage.removeItem("refresh_token")
      localStorage.removeItem("current_user_id")
      this.current_user = undefined
    },
  },
})
