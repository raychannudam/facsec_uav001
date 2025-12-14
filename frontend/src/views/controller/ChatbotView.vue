<template>
    <div class="fixed bottom-4 right-4 z-50">
        <!-- Chat Modal -->
        <transition name="modal">
            <div v-if="isOpen"
                class="absolute bottom-0 right-0 bg-white dark:bg-gray-800 rounded-lg shadow-2xl w-96 h-[600px] flex flex-col overflow-hidden border border-gray-200 dark:border-gray-700">
                <!-- Header -->
                <div class="bg-blue-600 dark:bg-blue-700 text-white p-4 flex justify-between items-center">
                    <div class="flex items-center gap-2">
                        <div class="w-8 h-8 bg-white dark:bg-gray-900 rounded-full flex items-center justify-center">
                            <svg class="w-6 h-6 text-blue-600 dark:text-blue-400" fill="none" stroke="currentColor"
                                stroke-width="2" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                                <path d="M12 8V4H8" />
                                <rect width="16" height="12" x="4" y="8" rx="2" />
                                <path d="M2 14h2" />
                                <path d="M20 14h2" />
                                <path d="M15 13v2" />
                                <path d="M9 13v2" />
                            </svg>
                        </div>
                        <div class="flex flex-col">
                            <span class="font-semibold">AI Assistant</span>
                            <!-- Connection Status -->
                            <span v-if="chatbotStore.isConnecting" class="text-xs text-blue-200">
                                Connecting...
                            </span>
                            <span v-else-if="chatbotStore.isConnected" class="text-xs text-green-200">
                                ● Connected
                            </span>
                            <span v-else class="text-xs text-red-200">
                                ○ Disconnected
                            </span>
                        </div>
                    </div>
                    <button @click="closeChat"
                        class="hover:bg-blue-700 dark:hover:bg-blue-800 rounded-full p-1 transition-colors">
                        <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="M6 18L18 6M6 6l12 12" />
                        </svg>
                    </button>
                </div>

                <!-- Chat Messages Area -->
                <div ref="messagesContainer" class="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900">
                    <div v-if="chatbotStore.isLoading" class="flex justify-center items-center h-full">
                        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 dark:border-blue-400">
                        </div>
                    </div>
                    <div v-else-if="!chatbotStore.currentSession"
                        class="flex justify-center items-center h-full text-gray-500 dark:text-gray-400">
                        <p>Starting chat session...</p>
                    </div>
                    <div v-else class="space-y-3">
                        <!-- Welcome Message -->
                        <div class="flex gap-2">
                            <div
                                class="w-8 h-8 bg-blue-600 dark:bg-blue-700 rounded-full flex items-center justify-center flex-shrink-0">
                                <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2"
                                    stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                                    <path d="M12 8V4H8" />
                                    <rect width="16" height="12" x="4" y="8" rx="2" />
                                    <path d="M2 14h2" />
                                    <path d="M20 14h2" />
                                    <path d="M15 13v2" />
                                    <path d="M9 13v2" />
                                </svg>
                            </div>
                            <div
                                class="bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm max-w-[70%] border border-gray-100 dark:border-gray-700">
                                <p class="text-sm text-gray-800 dark:text-gray-200">Hello! How can I assist you today?
                                </p>
                            </div>
                        </div>

                        <!-- ✅ NEW: Display messages -->
                        <div v-for="msg in chatbotStore.messages" :key="msg.id"
                            :class="['flex gap-2', msg.sender === 'user' ? 'justify-end' : '']">
                            <!-- Bot message -->
                            <template v-if="msg.sender === 'bot'">
                                <div
                                    class="w-8 h-8 bg-blue-600 dark:bg-blue-700 rounded-full flex items-center justify-center flex-shrink-0">
                                    <svg class="w-5 h-5 text-white" fill="none" stroke="currentColor" stroke-width="2"
                                        stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                                        <path d="M12 8V4H8" />
                                        <rect width="16" height="12" x="4" y="8" rx="2" />
                                        <path d="M2 14h2" />
                                        <path d="M20 14h2" />
                                        <path d="M15 13v2" />
                                        <path d="M9 13v2" />
                                    </svg>
                                </div>
                                <div
                                    class="bg-white dark:bg-gray-800 rounded-lg p-3 shadow-sm max-w-[70%] border border-gray-100 dark:border-gray-700">
                                    <p class="text-sm text-gray-800 dark:text-gray-200">{{ msg.text }}</p>
                                    <p class="text-xs text-gray-400 dark:text-gray-500 mt-1">
                                        {{ formatTime(msg.timestamp) }}
                                    </p>
                                </div>
                            </template>

                            <!-- User message -->
                            <template v-else>
                                <div
                                    class="bg-blue-600 dark:bg-blue-700 text-white rounded-lg p-3 shadow-sm max-w-[70%]">
                                    <p class="text-sm">{{ msg.text }}</p>
                                    <p class="text-xs text-blue-100 mt-1">
                                        {{ formatTime(msg.timestamp) }}
                                    </p>
                                </div>
                            </template>
                        </div>
                    </div>
                </div>

                <!-- Input Area -->
                <div class="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
                    <!-- ✅ NEW: Error message -->
                    <div v-if="chatbotStore.error" class="mb-2 text-xs text-red-600 dark:text-red-400">
                        {{ chatbotStore.error }}
                    </div>

                    <div class="flex gap-2">
                        <input v-model="message" type="text" placeholder="Type a message..."
                            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-full focus:outline-none focus:border-blue-600 dark:focus:border-blue-500 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                            @keyup.enter="sendMessage" :disabled="!chatbotStore.isConnected" />
                        <button @click="sendMessage" :disabled="!message.trim() || !chatbotStore.isConnected"
                            class="bg-blue-600 dark:bg-blue-700 text-white rounded-full p-2 hover:bg-blue-700 dark:hover:bg-blue-600 disabled:bg-gray-300 dark:disabled:bg-gray-600 disabled:cursor-not-allowed transition-colors">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        </transition>

        <!-- Floating Chat Button -->
        <transition name="button">
            <button v-if="!isOpen" @click="openChat"
                class="absolute bottom-0 right-0 bg-blue-600 dark:bg-blue-700 hover:bg-blue-700 dark:hover:bg-blue-600 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg transition-all hover:scale-110">
                <svg class="w-8 h-8" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"
                    stroke-linejoin="round" viewBox="0 0 24 24">
                    <path d="M12 8V4H8" />
                    <rect width="16" height="12" x="4" y="8" rx="2" />
                    <path d="M2 14h2" />
                    <path d="M20 14h2" />
                    <path d="M15 13v2" />
                    <path d="M9 13v2" />
                </svg>
            </button>
        </transition>
    </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, nextTick, watch } from 'vue';
import { useChatbotStore } from '@/stores/ChatbotStore';

const chatbotStore = useChatbotStore();
const isOpen = ref(false);
const message = ref('');
const messagesContainer = ref(null); // ✅ NEW: For auto-scroll

onMounted(async () => {
    // Initialize chat session when component mounts
    await chatbotStore.initializeSession();
});

// ✅ NEW: Cleanup on unmount
onBeforeUnmount(() => {
    chatbotStore.disconnectWebSocket();
});

const openChat = async () => {
    isOpen.value = true;

    // Ensure session is initialized when opening
    if (!chatbotStore.currentSession) {
        await chatbotStore.initializeSession();
    }

    // ✅ NEW: Connect WebSocket if not already connected
    if (!chatbotStore.isConnected && chatbotStore.currentConversation?.id) {
        chatbotStore.connectWebSocket();
    }
};

const closeChat = () => {
    isOpen.value = false;
};

const sendMessage = () => {
    if (!message.value.trim()) return;

    const success = chatbotStore.sendMessage(message.value);

    if (success) {
        message.value = ''; // Clear input

        // ✅ NEW: Auto-scroll to bottom after sending
        nextTick(() => {
            scrollToBottom();
        });
    }
};

// ✅ NEW: Auto-scroll to bottom when new messages arrive
const scrollToBottom = () => {
    if (messagesContainer.value) {
        messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
    }
};

// ✅ NEW: Watch messages and auto-scroll
watch(() => chatbotStore.messages.length, () => {
    nextTick(() => {
        scrollToBottom();
    });
});

// ✅ NEW: Format timestamp
const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit'
    });
};
</script>

<style scoped>
/* Modal transitions - smooth slide up from bottom */
.modal-enter-active {
    animation: modal-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.modal-leave-active {
    animation: modal-out 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes modal-in {
    0% {
        transform: translateY(100%) scale(0.8);
        opacity: 0;
    }

    100% {
        transform: translateY(0) scale(1);
        opacity: 1;
    }
}

@keyframes modal-out {
    0% {
        transform: translateY(0) scale(1);
        opacity: 1;
    }

    100% {
        transform: translateY(20px) scale(0.95);
        opacity: 0;
    }
}

/* Button transitions - smooth pop effect */
.button-enter-active {
    animation: button-in 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.button-leave-active {
    animation: button-out 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes button-in {
    0% {
        transform: scale(0) rotate(-180deg);
        opacity: 0;
    }

    100% {
        transform: scale(1) rotate(0deg);
        opacity: 1;
    }
}

@keyframes button-out {
    0% {
        transform: scale(1) rotate(0deg);
        opacity: 1;
    }

    100% {
        transform: scale(0) rotate(180deg);
        opacity: 0;
    }
}

/* ✅ NEW: Custom scrollbar */
.overflow-y-auto::-webkit-scrollbar {
    width: 6px;
}

.overflow-y-auto::-webkit-scrollbar-track {
    background: transparent;
}

.overflow-y-auto::-webkit-scrollbar-thumb {
    background: #cbd5e0;
    border-radius: 3px;
}

.dark .overflow-y-auto::-webkit-scrollbar-thumb {
    background: #4a5568;
}
</style>