// WebSocket URL configuration
const getWebSocketUrl = () => {
  const baseUrl = process.env.VUE_APP_API_URL || "http://localhost:8001";
  // Convert http://localhost:8001 → ws://localhost:8001
  return baseUrl.replace(/^http/, "ws");
};

export const WS_BASE_URL = getWebSocketUrl();
