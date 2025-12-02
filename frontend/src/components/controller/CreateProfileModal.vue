<template>
    <div v-if="isOpen" id="createProfileModal" tabindex="-1"
        class="fixed top-0 left-0 right-0 z-50 w-full p-4 overflow-x-hidden overflow-y-auto md:inset-0 h-full max-h-full bg-gray-900 bg-opacity-50 flex items-center justify-center">
        <div class="relative w-full max-w-md max-h-full">
            <!-- Modal content -->
            <div class="relative bg-white rounded-lg shadow dark:bg-gray-700">
                <!-- Modal header -->
                <div class="flex items-center justify-between p-4 border-b dark:border-gray-600">
                    <h3 class="text-lg font-semibold text-gray-900 dark:text-white">
                        Create New Profile
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
                <form @submit.prevent="handleSubmit" class="p-6">
                    <div class="mb-4">
                        <label for="profileName" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white">
                            Profile Name <span class="text-red-500">*</span>
                        </label>
                        <input v-model="formData.name" type="text" id="profileName"
                            class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white"
                            placeholder="Enter profile name" required>
                        <p v-if="errors.name" class="mt-2 text-sm text-red-600 dark:text-red-500">
                            {{ errors.name }}
                        </p>
                    </div>

                    <!-- Modal footer -->
                    <div class="flex items-center justify-end space-x-2">
                        <button @click="closeModal" type="button"
                            class="text-gray-500 bg-white hover:bg-gray-100 focus:ring-4 focus:outline-none focus:ring-gray-200 rounded-lg border border-gray-200 text-sm font-medium px-5 py-2.5 hover:text-gray-900 dark:bg-gray-700 dark:text-gray-300 dark:border-gray-500 dark:hover:text-white dark:hover:bg-gray-600">
                            Cancel
                        </button>
                        <button type="submit"
                            class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center dark:bg-blue-600 dark:hover:bg-blue-700">
                            Create
                        </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    }
});

const emit = defineEmits(['close', 'create']);

const formData = ref({
    name: ''
});

const errors = ref({
    name: ''
});

const closeModal = () => {
    resetForm();
    emit('close');
};

const handleSubmit = () => {
    // Validate
    errors.value.name = '';

    if (!formData.value.name.trim()) {
        errors.value.name = 'Profile name is required';
        return;
    }

    if (formData.value.name.trim().length < 3) {
        errors.value.name = 'Profile name must be at least 3 characters';
        return;
    }

    // Emit create event with form data
    emit('create', {
        name: formData.value.name.trim(),
        description: ''
    });

    resetForm();
};

const resetForm = () => {
    formData.value = {
        name: ''
    };
    errors.value = {
        name: ''
    };
};

// Reset form when modal is closed
watch(() => props.isOpen, (newVal) => {
    if (!newVal) {
        resetForm();
    }
});
</script>