import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/plugins/api";

export const useChatbotStore = defineStore("chatbot", () => {
  const currentSession = ref(null);
  const currentConversation = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

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

  // Initialize session (called when user opens chat)
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

  // Reset chat (useful for clearing session)
  const resetChat = () => {
    currentSession.value = null;
    currentConversation.value = null;
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
    isLoading,
    error,

    // Actions
    initializeSession,
    createSession,
    createConversation,
    checkSession,
    resetChat,
  };
});
