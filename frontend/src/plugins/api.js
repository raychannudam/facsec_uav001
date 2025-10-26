import axios from "axios";
import router from "@/router";

const api = axios.create({
  baseURL: process.env.VUE_APP_API_URL || "http://localhost:3000",
});

const refreshClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || "http://localhost:3000",
});

api.interceptors.request.use(
  (config) => {
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

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (
      error.response?.status === 401 &&
      !originalRequest._retry &&
      !originalRequest.url.includes("/token")
    ) {
      originalRequest._retry = true;

      const refreshToken = localStorage.getItem("refresh_token");

      if (!refreshToken) {
        localStorage.clear();
        router.push({ name: "sign-in" });
        return Promise.reject(error);
      }

      try {
        const response = await refreshClient.post(
          `/api/v1/token/refresh?refresh_token=${refreshToken}`
        );

        const { access_token, refresh_token } = response.data;

        // Store new tokens
        localStorage.setItem("access_token", access_token);
        localStorage.setItem("refresh_token", refresh_token);

        // Update original request with new token
        originalRequest.headers.Authorization = `Bearer ${access_token}`;

        // Retry original request
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.clear();
        router.push({ name: "sign-in" });
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

export default api;
