<template>
    <div class="flex flex-col items-center p-3 rounded-lg cursor-pointer transition-all duration-200 select-none h-full shadow-sm"
        :class="isActive
            ? 'bg-blue-200 dark:bg-blue-800/40 text-blue-700 dark:text-blue-300 scale-95 shadow-inner'
            : 'bg-blue-50 dark:bg-blue-900/10 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-800/20 hover:shadow-md'"
        @click="handleClick">
        <!-- Title with extra icon, top-left -->
        <div class="flex items-center gap-1 mb-3 w-full justify-start">
            <span class="material-symbols-outlined text-base">touch_app</span>
            <span class="font-medium">{{ button.name }}</span>
        </div>

        <!-- Power Icon - centered -->
        <span class="material-symbols-outlined text-5xl transition-transform" :class="isActive ? 'scale-90' : ''">
            power_settings_new
        </span>

        <!-- Status indicator - centered -->
        <div class="mt-2 text-xs font-semibold">
            {{ isActive ? 'ACTIVE' : 'READY' }}
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits } from 'vue'

const props = defineProps({
    button: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['trigger'])
const isActive = ref(false)

const handleClick = () => {
    emit('trigger', {
        id: props.button.id,
        name: props.button.name,
        payload: props.button.onPayload
    })
    isActive.value = true

    setTimeout(() => {
        emit('trigger', {
            id: props.button.id,
            name: props.button.name,
            payload: props.button.offPayload
        })
        isActive.value = false
    }, 1000)
}
</script>
