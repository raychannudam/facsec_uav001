<template>
    <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
        <span class="font-medium text-gray-700">{{ switchData.name }}</span>
        <button @click="toggle" :class="[
            'relative inline-flex h-6 w-11 items-center rounded-full transition-colors focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-offset-2',
            isOn ? 'bg-green-600' : 'bg-gray-300'
        ]">
            <span :class="[
                'inline-block h-4 w-4 transform rounded-full bg-white transition-transform',
                isOn ? 'translate-x-6' : 'translate-x-1'
            ]" />
        </button>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue';

const props = defineProps({
    switchData: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['toggle']);

const isOn = ref(false);

const toggle = () => {
    isOn.value = !isOn.value;
    const payload = isOn.value ? props.switchData.onPayload : props.switchData.offPayload;
    emit('toggle', {
        id: props.switchData.id,
        name: props.switchData.name,
        state: isOn.value ? 'ON' : 'OFF',
        payload: payload
    });
};
</script>