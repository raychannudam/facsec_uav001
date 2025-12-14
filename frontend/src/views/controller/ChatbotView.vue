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
                        <span class="font-semibold">AI Assistant</span>
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
                <div class="flex-1 overflow-y-auto p-4 bg-gray-50 dark:bg-gray-900">
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

                        <!-- Sample messages (replace with actual messages later) -->
                        <!-- User message example -->
                        <!-- <div class="flex gap-2 justify-end">
                            <div class="bg-blue-600 dark:bg-blue-700 text-white rounded-lg p-3 shadow-sm max-w-[70%]">
                                <p class="text-sm">This is a user message</p>
                            </div>
                        </div> -->
                    </div>
                </div>

                <!-- Input Area -->
                <div class="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
                    <div class="flex gap-2">
                        <input v-model="message" type="text" placeholder="Type a message..."
                            class="flex-1 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-full focus:outline-none focus:border-blue-600 dark:focus:border-blue-500 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-gray-100 placeholder-gray-400 dark:placeholder-gray-500"
                            @keyup.enter="sendMessage" />
                        <button @click="sendMessage" :disabled="!message.trim()"
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
import { ref, onMounted } from 'vue';
import { useChatbotStore } from '@/stores/ChatbotStore';

const chatbotStore = useChatbotStore();
const isOpen = ref(false);
const message = ref('');

onMounted(async () => {
    // Initialize chat session when component mounts
    await chatbotStore.initializeSession();
});

const openChat = async () => {
    isOpen.value = true;
    // Ensure session is initialized when opening
    if (!chatbotStore.currentSession) {
        await chatbotStore.initializeSession();
    }
};

const closeChat = () => {
    isOpen.value = false;
};

const sendMessage = () => {
    if (message.value.trim()) {
        console.log('Sending message:', message.value);
        // TODO: Implement message sending logic
        message.value = '';
    }
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
</style>