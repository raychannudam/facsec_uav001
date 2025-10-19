<template>
    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg hover:bg-gray-100 transition-colors">
        <span class="font-medium text-gray-700">{{ button.name }}</span>
        <button
            class="flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg font-medium transition-colors shadow-sm hover:shadow-md active:scale-95 transform"
            @click="handleClick">
            <svg xmlns="http://www.w3.org/2000/svg" class="h-4 w-4" fill="none" viewBox="0 0 24 24"
                stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Trigger
        </button>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    button: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['trigger']);

const handleClick = () => {
    emit('trigger', {
        id: props.button.id,
        name: props.button.name,
        payload: props.button.onPayload
    });
};
</script>