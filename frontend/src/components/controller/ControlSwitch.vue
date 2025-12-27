<template name="ControlSwitch">
    <div class="flex flex-col items-center p-3 rounded-lg select-none cursor-pointer h-32 transition-colors"
        :class="isOn ? 'bg-green-50 dark:bg-green-900/20' : 'bg-red-50 dark:bg-red-900/20'" @click="toggle">
        <!-- Name with hand-click icon, top-left -->
        <div class="flex items-center gap-1 w-full mb-2"
            :class="isOn ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
            <span class="material-symbols-outlined text-base">touch_app</span>
            <span class="font-medium text-sm">{{ switchData.name }}</span>
        </div>

        <!-- Toggle Switch, centered -->
        <div class="flex-1 flex items-center justify-center">
            <div :class="[
                'relative inline-flex h-10 w-20 items-center rounded-full transition-all duration-300 ease-in-out shadow-lg',
                isOn ? 'bg-green-600 dark:bg-green-500' : 'bg-red-600 dark:bg-red-500'
            ]">
                <span :class="[
                    'inline-block h-8 w-8 transform rounded-full bg-white transition-transform duration-300 ease-in-out shadow-md',
                    isOn ? 'translate-x-[2.75rem]' : 'translate-x-1'
                ]" />
            </div>
        </div>

        <!-- Status Text, centered -->
        <div class="text-xs font-semibold"
            :class="isOn ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'">
            {{ isOn ? 'ON' : 'OFF' }}
        </div>
    </div>
</template>

<script setup>
import { ref, defineProps, defineEmits, computed } from 'vue'

const props = defineProps({
    switchData: {
        type: Object,
        required: true
    }
})

const emit = defineEmits(['toggle'])
const isOn = computed(() => props.switchData.additionalConfig?.latest_state === "1");
const toggle = () => {
    const newState = !isOn.value;
    const payload = newState ? props.switchData.onPayload : props.switchData.offPayload;

    // Emit the change
    emit('toggle', {
        id: props.switchData.id,
        name: props.switchData.name,
        payload: payload
    });
    
    props.switchData.additionalConfig.latest_state = newState ? "1" : "0";
}
</script>