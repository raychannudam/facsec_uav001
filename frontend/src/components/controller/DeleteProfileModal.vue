<template>
    <div v-if="isOpen" id="deleteProfileModal" tabindex="-1"
        class="fixed top-0 left-0 right-0 z-50 w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-full max-h-full bg-gray-900 bg-opacity-50 flex items-center justify-center">
        <div class="relative w-full max-w-md max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 border-b dark:border-gray-600">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        Delete Profile
                    </h3>
                    <button @click="closeModal" type="button"
                        class="text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm w-8 h-8 inline-flex justify-center items-center dark:hover:bg-gray-600 dark:hover:text-white">
                        <svg class="w-3 h-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 14 14">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 6 6m0 0 6 6M7 7l6-6M7 7l-6 6" />
                        </svg>
                    </button>
                </div>

                <!-- Modal body -->
                <div class="p-6">
                    <!-- Warning Icon -->
                    <div class="flex justify-center mb-4">
                        <div class="flex items-center justify-center w-12 h-12 bg-red-100 rounded-full dark:bg-red-900">
                            <span
                                class="material-symbols-outlined text-3xl text-red-600 dark:text-red-300">delete</span>
                        </div>
                    </div>

                    <!-- Warning Text -->
                    <div class="text-center mb-4">
                        <p class="text-sm text-gray-500 dark:text-gray-400 mb-2">
                            Are you sure you want to delete
                        </p>
                        <p class="text-base font-semibold text-gray-900 dark:text-white">
                            "{{ profileName }}"?
                        </p>
                    </div>

                    <!-- Confirmation Input -->
                    <div class="mb-6">
                        <label for="confirmInput" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                            Type <span class="font-bold text-red-600">DELETE</span> to confirm
                        </label>
                        <input v-model="confirmText" type="text" id="confirmInput"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-red-500 focus:border-red-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                            placeholder="Type DELETE">
                    </div>

                    <!-- Modal footer -->
                    <div class="flex items-center justify-end space-x-2">
                        <button @click="closeModal" type="button"
                            class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600">
                            Cancel
                        </button>
                        <button @click="handleDelete" :disabled="!isConfirmed" type="button"
                            class="text-white bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-red-600 dark:hover:bg-red-700 disabled:opacity-50 disabled:cursor-not-allowed">
                            Delete
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue';

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    profileName: {
        type: String,
        default: ''
    }
});

const emit = defineEmits(['close', 'delete']);

const confirmText = ref('');

const isConfirmed = computed(() => {
    return confirmText.value.trim().toUpperCase() === 'DELETE';
});

const closeModal = () => {
    confirmText.value = '';
    emit('close');
};

const handleDelete = () => {
    if (!isConfirmed.value) {
        return;
    }

    emit('delete');
    confirmText.value = '';
};

// Reset confirmation text when modal is closed
watch(() => props.isOpen, (newVal) => {
    if (!newVal) {
        confirmText.value = '';
    }
});
</script>