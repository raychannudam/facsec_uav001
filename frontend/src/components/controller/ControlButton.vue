<template name="ControlButton">
    <div class="flex flex-col items-center p-3 rounded-lg cursor-pointer transition-all duration-200 select-none h-32 shadow-sm"
        :class="isActive
            ? 'bg-blue-200 dark:bg-blue-800/40 text-blue-700 dark:text-blue-300 scale-95 shadow-inner'
            : 'bg-blue-50 dark:bg-blue-400/10 text-blue-600 dark:text-blue-400 hover:bg-blue-100 dark:hover:bg-blue-800/20 hover:shadow-md'"
        @mousedown="handleMouseDown" @mouseup="handleMouseUp" @mouseleave="handleMouseUp" @touchstart="handleMouseDown"
        @touchend="handleMouseUp" tabindex="0">
        <!-- Title with extra icon, top-left -->
        <div class="flex items-center gap-1 mb-2 w-full justify-start">
            <span class="material-symbols-outlined text-base">touch_app</span>
            <span class="font-medium text-sm">{{ button.name }}</span>
        </div>

        <!-- Power Icon - centered -->
        <span class="material-symbols-outlined text-4xl transition-transform flex-1 flex items-center justify-center"
            :class="isActive ? 'scale-90' : ''">
            power_settings_new
        </span>

        <!-- Status indicator - centered -->
        <div class="text-xs font-semibold">
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
const holdInterval = ref(null)

const handleMouseDown = (event) => {
    event.preventDefault() // Prevent text selection while holding

    if (holdInterval.value) return // Already holding

    isActive.value = true

    // Emit onPayload immediately when mouse is pressed
    emit('trigger', {
        id: props.button.id,
        name: props.button.name,
        payload: props.button.onPayload
    })

    // Continue emitting onPayload every 100ms while holding
    holdInterval.value = setInterval(() => {
        emit('trigger', {
            id: props.button.id,
            name: props.button.name,
            payload: props.button.onPayload
        })
    }, 100)
}

const handleMouseUp = (event) => {
    if (holdInterval.value) {
        clearInterval(holdInterval.value)
        holdInterval.value = null
    }

    if (isActive.value) {
        // Emit offPayload when mouse is released
        emit('trigger', {
            id: props.button.id,
            name: props.button.name,
            payload: props.button.offPayload
        })
        isActive.value = false
    }
}
</script>