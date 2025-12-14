import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/plugins/api";
import { WS_BASE_URL } from "@/plugins/websocket";

export const useChatbotStore = defineStore("chatbot", () => {
  const currentSession = ref(null);
  const currentConversation = ref(null);
  const messages = ref([]); // NEW: Store messages
  const isLoading = ref(false);
  const error = ref(null);

  // NEW: WebSocket state
  const ws = ref(null);
  const isConnected = ref(false);
  const isConnecting = ref(false);

  const getUserId = () => {
    return Number(localStorage.getItem("current_user_id"));
  };

  // Check if session exists
  const checkSession = async (sessionId) => {
    try {
      const response = await api.get(`/api/v1/chat/sessions/${sessionId}`);
      return response.data;
    } catch (err) {
      console.error("Error checking session:", err);
      return null;
    }
  };

  // Create new session
  const createSession = async (userId) => {
    let status = "fail";
    let message = "";
    let data = undefined;
    try {
      const response = await api.post(
        `/api/v1/chat/sessions/?user_id=${userId}`
      );
      currentSession.value = response.data;
      data = response.data;
      status = "success";
      message = "Successfully created chat session!";

      // Store session ID in localStorage for future reference
      localStorage.setItem(`chat_session_${userId}`, response.data.id);
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create chat session!";
      console.error("Error creating session:", err);
      error.value = message;
    }
    return { status, message, data };
  };

  // Create conversation
  const createConversation = async (sessionId, userId) => {
    let status = "fail";
    let message = "";
    let data = undefined;
    try {
      const response = await api.post(
        `/api/v1/chat/conversations/?session_id=${sessionId}&user_id=${userId}`
      );
      currentConversation.value = response.data;
      data = response.data;
      status = "success";
      message = "Successfully created conversation!";
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create conversation!";
      console.error("Error creating conversation:", err);
      error.value = message;
    }
    return { status, message, data };
  };

  // Initialize session
  const initializeSession = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const userId = getUserId();
      if (!userId) {
        error.value = "User ID not found";
        isLoading.value = false;
        return { status: "fail", message: "User ID not found" };
      }

      // Check if we have a stored session ID
      const storedSessionId = localStorage.getItem(`chat_session_${userId}`);

      if (storedSessionId) {
        // Try to retrieve existing session
        const existingSession = await checkSession(storedSessionId);

        if (existingSession) {
          console.log("✅ Found existing session:", existingSession);
          currentSession.value = existingSession;
          isLoading.value = false;
          return {
            status: "success",
            message: "Session loaded",
            data: existingSession,
          };
        } else {
          // Session doesn't exist anymore, remove from localStorage
          localStorage.removeItem(`chat_session_${userId}`);
        }
      }

      // No existing session found, create new one
      console.log("🔄 Creating new session for user:", userId);
      const sessionResult = await createSession(userId);

      if (sessionResult.status === "success") {
        // Create initial conversation
        console.log("🔄 Creating initial conversation...");
        await createConversation(sessionResult.data.id, userId);
      }

      isLoading.value = false;
      return sessionResult;
    } catch (err) {
      console.error("Error initializing session:", err);
      error.value = "Failed to initialize chat session";
      isLoading.value = false;
      return { status: "fail", message: error.value };
    }
  };

  // NEW: Connect WebSocket
  const connectWebSocket = () => {
    if (!currentConversation.value?.id) {
      console.error("❌ No conversation ID available");
      error.value = "No conversation ID";
      return;
    }

    if (ws.value?.readyState === WebSocket.OPEN) {
      console.log("✅ WebSocket already connected");
      return;
    }

    isConnecting.value = true;
    error.value = null;

    const conversationId = currentConversation.value.id;
    const wsUrl = `${WS_BASE_URL}/api/v1/chat/ws/${conversationId}`;

    console.log("🔌 Connecting to WebSocket:", wsUrl);

    try {
      ws.value = new WebSocket(wsUrl);

      ws.value.onopen = () => {
        console.log("✅ WebSocket connected!");
        isConnected.value = true;
        isConnecting.value = false;
        error.value = null;
      };

      ws.value.onmessage = (event) => {
        console.log("📩 Received message:", event.data);

        try {
          const data = JSON.parse(event.data);

          // Add bot message to messages array
          // TODO: Adjust this based on backend's actual response format
          messages.value.push({
            id: data.id || Date.now(),
            text: data.message || data.response || data.user_prompt,
            sender: "bot",
            timestamp: data.timestamp || new Date().toISOString(),
          });

          console.log("💬 Bot message added:", messages.value);
        } catch (err) {
          console.error("❌ Error parsing message:", err);
          // If it's plain text, just add it
          messages.value.push({
            id: Date.now(),
            text: event.data,
            sender: "bot",
            timestamp: new Date().toISOString(),
          });
        }
      };

      ws.value.onerror = (event) => {
        console.error("❌ WebSocket error:", event);
        error.value = "WebSocket connection error";
        isConnecting.value = false;
      };

      ws.value.onclose = (event) => {
        console.log("🔌 WebSocket closed:", event.code, event.reason);
        isConnected.value = false;
        isConnecting.value = false;

        // Auto-reconnect if not a normal closure
        if (event.code !== 1000 && currentConversation.value?.id) {
          console.log("🔄 Reconnecting in 3 seconds...");
          setTimeout(() => {
            connectWebSocket();
          }, 3000);
        }
      };
    } catch (err) {
      console.error("❌ Failed to create WebSocket:", err);
      error.value = "Failed to connect WebSocket";
      isConnecting.value = false;
    }
  };

  // ✅ NEW: Send message via WebSocket
  const sendMessage = (messageText) => {
    if (!messageText.trim()) {
      console.warn("⚠️ Empty message");
      return false;
    }

    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      console.error("❌ WebSocket not connected");
      error.value = "Not connected to chat";
      return false;
    }

    const userId = getUserId();
    if (!userId) {
      console.error("❌ No user ID");
      error.value = "User ID not found";
      return false;
    }

    try {
      const payload = {
        user_id: userId,
        user_prompt: messageText,
      };

      console.log("📤 Sending message:", payload);
      ws.value.send(JSON.stringify(payload));

      // Add user message to UI immediately (optimistic update)
      messages.value.push({
        id: Date.now(),
        text: messageText,
        sender: "user",
        timestamp: new Date().toISOString(),
      });

      console.log("✅ Message sent!");
      return true;
    } catch (err) {
      console.error("❌ Failed to send message:", err);
      error.value = "Failed to send message";
      return false;
    }
  };

  // ✅ NEW: Disconnect WebSocket
  const disconnectWebSocket = () => {
    if (ws.value) {
      console.log("🔌 Disconnecting WebSocket...");
      ws.value.close(1000, "User disconnected");
      ws.value = null;
    }
    isConnected.value = false;
  };

  // Reset chat (useful for clearing session)
  const resetChat = () => {
    disconnectWebSocket(); // ✅ NEW: Disconnect WebSocket
    currentSession.value = null;
    currentConversation.value = null;
    messages.value = []; // ✅ NEW: Clear messages
    error.value = null;
    const userId = getUserId();
    if (userId) {
      localStorage.removeItem(`chat_session_${userId}`);
    }
  };

  return {
    // State
    currentSession,
    currentConversation,
    messages, // ✅ NEW
    isLoading,
    error,

    // ✅ NEW: WebSocket state
    isConnected,
    isConnecting,

    // Actions
    initializeSession,
    createSession,
    createConversation,
    checkSession,
    resetChat,

    // ✅ NEW: WebSocket actions
    connectWebSocket,
    sendMessage,
    disconnectWebSocket,
  };
});
