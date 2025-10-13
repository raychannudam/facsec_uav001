import axios from "axios";
import router from "@/router";

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || "http://localhost:3000"
});

// Request interceptor — attach token unless skipped
api.interceptors.request.use(
  (config) => {
    // Skip attaching token for login/signup
    if (config.headers.skipAuth) {
      delete config.headers.skipAuth;
      return config;
    }
    const token = localStorage.getItem("access_token");
    if (token) config.headers.Authorization = `Bearer ${token}`;
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor — handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.clear();
      router.push({ name: "sign-in" });
    }
    return Promise.reject(error);
  }
);

export default api;
