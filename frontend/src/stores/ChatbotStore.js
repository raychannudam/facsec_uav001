import { defineStore } from "pinia";
import { ref } from "vue";
import api from "@/plugins/api";

export const useChatbotStore = defineStore("chatbot", () => {
  const currentSession = ref(null);
  const currentConversation = ref(null);
  const messages = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  // WebSocket state
  const ws = ref(null);
  const isConnected = ref(false);
  const isConnecting = ref(false);

  const getUserId = () => {
    return Number(localStorage.getItem("current_user_id"));
  };

  // Get WebSocket URL from environment or default
  const getWebSocketUrl = () => {
    const wsUrl = process.env.VUE_APP_WS_URL || "ws://localhost:8001";
    console.log("🔧 WebSocket Base URL:", wsUrl);
    return wsUrl;
  };

  // Get conversation with messages for current user
  const getUserConversation = async () => {
    try {
      const response = await api.get("/api/v1/chat/conversations/");
      return response.data;
    } catch (err) {
      console.error("❌ Error fetching conversation:", err);
      return null;
    }
  };

  // Create new session
  const createSession = async () => {
    let status = "fail";
    let message = "";
    let data = undefined;
    try {
      const response = await api.post("/api/v1/chat/sessions/");
      currentSession.value = response.data;
      data = response.data;
      status = "success";
      message = "Successfully created chat session!";
      console.log("✅ Session created:", data);
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create chat session!";
      console.error("❌ Error creating session:", err);
      error.value = message;
    }
    return { status, message, data };
  };

  // Create conversation
  const createConversation = async (sessionId) => {
    let status = "fail";
    let message = "";
    let data = undefined;
    try {
      const response = await api.get(`/api/v1/chat/sessions/${sessionId}`);
      currentConversation.value = response.data;
      data = response.data;
      status = "success";
      message = "Successfully created conversation!";
      console.log("✅ Conversation created:", data);
    } catch (err) {
      status = "fail";
      message = err.response?.data?.detail || "Failed to create conversation!";
      console.error("❌ Error creating conversation:", err);
      error.value = message;
    }
    return { status, message, data };
  };

  // Initialize session when opening chatbot
  const initializeSession = async () => {
    isLoading.value = true;
    error.value = null;

    try {
      const userId = getUserId();
      if (!userId) {
        error.value = "User ID not found. Please login again.";
        isLoading.value = false;
        return { status: "fail", message: error.value };
      }

      console.log("🔍 Checking for existing conversation for user:", userId);

      // Check if user has an existing conversation
      const conversation = await getUserConversation();

      if (conversation && conversation.id) {
        // User has existing conversation, load it
        console.log("✅ User has existing conversation, loading...");

        currentConversation.value = conversation;
        currentSession.value = { id: conversation.session_id };

        console.log("📜 Loading message history from conversation");

        // ✅ FIX: Transform backend messages correctly
        // Each message has BOTH user_prompt and response, so we need to create TWO UI messages per backend message
        messages.value = [];
        (conversation.messages || []).forEach((msg) => {
          // Add user message
          if (msg.user_prompt) {
            messages.value.push({
              id: `user-${msg.id}`,
              text: msg.user_prompt,
              sender: "user",
              timestamp: msg.timestamp,
            });
          }

          // Add bot response
          if (msg.response) {
            messages.value.push({
              id: `bot-${msg.id}`,
              text: msg.response,
              sender: "bot",
              timestamp: msg.timestamp,
            });
          }
        });

        console.log(
          `✅ Loaded ${messages.value.length} message(s) from ${
            conversation.messages?.length || 0
          } backend messages`
        );

        // Connect to WebSocket
        try {
          connectWebSocket();
        } catch (wsError) {
          console.warn(
            "⚠️ WebSocket connection failed, but continuing...",
            wsError
          );
          error.value =
            "Chat loaded, but live connection failed. Messages may be delayed.";
        }

        isLoading.value = false;
        return {
          status: "success",
          message: "Conversation loaded successfully",
          data: conversation,
        };
      }

      // No existing conversation, create new session and conversation
      console.log("🆕 No conversation found, creating new session...");

      const sessionResult = await createSession();

      if (sessionResult.status === "success") {
        console.log("🆕 Creating new conversation...");
        const conversationResult = await createConversation(
          sessionResult.data.id
        );

        if (conversationResult.status === "success") {
          // Connect to WebSocket
          try {
            connectWebSocket();
          } catch (wsError) {
            console.warn(
              "⚠️ WebSocket connection failed, but continuing...",
              wsError
            );
            error.value =
              "Chat created, but live connection failed. Please check your connection.";
          }

          isLoading.value = false;
          return {
            status: "success",
            message: "New chat session created",
            data: conversationResult.data,
          };
        } else {
          isLoading.value = false;
          return conversationResult;
        }
      }

      isLoading.value = false;
      return sessionResult;
    } catch (err) {
      console.error("❌ Error initializing session:", err);
      error.value = "Failed to initialize chat session";
      isLoading.value = false;
      return { status: "fail", message: error.value };
    }
  };

  // Connect WebSocket
  const connectWebSocket = () => {
    if (!currentConversation.value?.id) {
      console.error("❌ No conversation ID available for WebSocket connection");
      error.value = "No conversation ID";
      return;
    }

    if (ws.value?.readyState === WebSocket.OPEN) {
      console.log("✅ WebSocket already connected");
      return;
    }

    if (isConnecting.value) {
      console.log("⏳ WebSocket connection already in progress");
      return;
    }

    isConnecting.value = true;
    error.value = null;

    const conversationId = currentConversation.value.id;
    const accessToken = localStorage.getItem("access_token");
    const wsBaseUrl = getWebSocketUrl();
    const wsUrl = `${wsBaseUrl}/api/v1/chat/ws/${conversationId}?token=${accessToken}`;

    console.log("🔌 Attempting WebSocket connection to:", wsUrl);
    console.log("🔧 Conversation ID:", conversationId);

    try {
      ws.value = new WebSocket(wsUrl);

      // Set a connection timeout
      const connectionTimeout = setTimeout(() => {
        if (ws.value && ws.value.readyState !== WebSocket.OPEN) {
          console.error("❌ WebSocket connection timeout");
          ws.value.close();
          isConnecting.value = false;
          error.value =
            "Connection timeout. Please check if the chat server is running.";
        }
      }, 10000); // 10 second timeout

      ws.value.onopen = () => {
        clearTimeout(connectionTimeout);
        console.log("✅ WebSocket connected successfully!");
        isConnected.value = true;
        isConnecting.value = false;
        error.value = null;
      };

      ws.value.onmessage = (event) => {
        console.log("📩 Received message from server:", event.data);

        try {
          const data = JSON.parse(event.data);

          // Add bot response to messages
          const botMessage = {
            id: data.id || Date.now(),
            text:
              data.response || data.message || data.bot_response || event.data,
            sender: "bot",
            // ✅ FIX: Use server timestamp directly (it's already in UTC ISO format)
            timestamp: data.timestamp || new Date().toISOString(),
          };

          messages.value.push(botMessage);
          console.log("💬 Bot message added to UI:", botMessage.text);
          console.log("🕐 Bot message timestamp:", botMessage.timestamp);
        } catch (err) {
          console.error("❌ Error parsing WebSocket message:", err);
          // If it's plain text, just add it as-is
          messages.value.push({
            id: Date.now(),
            text: event.data,
            sender: "bot",
            timestamp: new Date().toISOString(),
          });
        }
      };

      ws.value.onerror = (event) => {
        clearTimeout(connectionTimeout);
        console.error("❌ WebSocket error details:", {
          readyState: ws.value?.readyState,
          url: wsUrl,
          event: event,
        });

        // More helpful error messages based on common issues
        if (wsUrl.includes("localhost")) {
          error.value =
            "Cannot connect to chat server on localhost:8001. Is the server running?";
        } else {
          error.value =
            "Chat server connection failed. Please try again later.";
        }

        isConnecting.value = false;
      };

      ws.value.onclose = (event) => {
        clearTimeout(connectionTimeout);
        console.log("🔌 WebSocket closed:", {
          code: event.code,
          reason: event.reason,
          wasClean: event.wasClean,
        });

        isConnected.value = false;
        isConnecting.value = false;

        // Don't show error for normal closures
        if (event.code === 1000) {
          console.log("✅ WebSocket closed normally");
          return;
        }

        // Auto-reconnect only if it was previously connected
        if (
          event.code !== 1000 &&
          currentConversation.value?.id &&
          isConnected.value === false
        ) {
          console.log("🔄 Attempting to reconnect in 5 seconds...");
          setTimeout(() => {
            if (currentConversation.value?.id && !isConnected.value) {
              console.log("🔄 Reconnecting now...");
              connectWebSocket();
            }
          }, 5000);
        }
      };
    } catch (err) {
      console.error("❌ Failed to create WebSocket connection:", err);
      error.value = "Failed to connect to chat server: " + err.message;
      isConnecting.value = false;
    }
  };

  // Send message via WebSocket
  const sendMessage = (messageText) => {
    if (!messageText.trim()) {
      console.warn("⚠️ Cannot send empty message");
      return false;
    }

    if (!ws.value || ws.value.readyState !== WebSocket.OPEN) {
      console.error("❌ WebSocket not connected. State:", ws.value?.readyState);
      error.value = "Not connected to chat server. Trying to reconnect...";

      // Try to reconnect
      if (currentConversation.value?.id) {
        console.log("🔄 Attempting to reconnect...");
        connectWebSocket();
      }
      return false;
    }

    try {
      const payload = {
        user_prompt: messageText,
      };

      console.log("📤 Sending message to server:", payload);
      ws.value.send(JSON.stringify(payload));

      // ✅ FIX: Add user message with current timestamp (will be updated by server response anyway)
      const userMessage = {
        id: `temp-${Date.now()}`,
        text: messageText,
        sender: "user",
        timestamp: new Date().toISOString(), // This will be synced with bot response timestamp
      };

      messages.value.push(userMessage);
      console.log("✅ User message added to UI");

      error.value = null;
      return true;
    } catch (err) {
      console.error("❌ Failed to send message:", err);
      error.value = "Failed to send message: " + err.message;
      return false;
    }
  };

  // Disconnect WebSocket
  const disconnectWebSocket = () => {
    if (ws.value) {
      console.log("🔌 Disconnecting WebSocket...");
      ws.value.close(1000, "User disconnected");
      ws.value = null;
    }
    isConnected.value = false;
    isConnecting.value = false;
  };

  // Reset chat (useful for clearing session)
  const resetChat = () => {
    console.log("🔄 Resetting chat...");
    disconnectWebSocket();
    currentSession.value = null;
    currentConversation.value = null;
    messages.value = [];
    error.value = null;
    isLoading.value = false;
  };

  return {
    // State
    currentSession,
    currentConversation,
    messages,
    isLoading,
    error,

    // WebSocket state
    isConnected,
    isConnecting,

    // Actions
    initializeSession,
    createSession,
    createConversation,
    getUserConversation,
    resetChat,

    // WebSocket actions
    connectWebSocket,
    sendMessage,
    disconnectWebSocket,
  };
});
