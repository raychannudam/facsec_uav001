<template name="ControlSlider">
    <div class="p-3 bg-gray-50 dark:bg-gray-700 rounded-lg flex flex-col justify-center h-32 transition-colors">
        <!-- Title with hand icon -->
        <div class="flex items-center justify-between mb-2">
            <div class="flex items-center gap-1">
                <span class="material-symbols-outlined text-sm text-purple-800 dark:text-purple-300">touch_app</span>
                <span class="font-medium text-sm text-purple-800 dark:text-purple-300">{{ slider.name }}</span>
            </div>

            <!-- Current value -->
            <span
                class="bg-purple-100 dark:bg-purple-900 text-purple-800 dark:text-purple-200 text-xs font-semibold px-2 py-1 rounded-full">
                {{ value }}
            </span>
        </div>

        <!-- Slider -->
        <input type="range" :min="minValue" :max="maxValue" v-model="value"
            class="w-full h-2 bg-gray-200 dark:bg-gray-600 rounded-lg appearance-none cursor-pointer slider mb-2"
            @input="handleChange" :aria-valuemin="minValue" :aria-valuemax="maxValue" :aria-valuenow="value" />

        <!-- Min/Max labels -->
        <div class="flex justify-between text-xs text-gray-500 dark:text-gray-400">
            <span>{{ minValue }}</span>
            <span>{{ maxValue }}</span>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, defineProps, defineEmits, watch } from 'vue';

const props = defineProps({
    slider: {
        type: Object,
        required: true
    }
});

const emit = defineEmits(['change']);

const clamp = (v, a, b) => Math.max(Math.min(v, Math.max(a, b)), Math.min(a, b));

const minValue = computed(() => {
    const raw = Number(props.slider?.minPayload);
    return Number.isFinite(raw) ? Math.floor(raw) : 0;
});
const maxValue = computed(() => {
    const raw = Number(props.slider?.maxPayload);
    return Number.isFinite(raw) ? Math.floor(raw) : 100;
});

const value = ref(0);

watch([minValue, maxValue], ([mn, mx]) => {
    const low = Math.min(mn, mx);
    const high = Math.max(mn, mx);
    if (!Number.isFinite(value.value)) {
        value.value = Math.floor((low + high) / 2);
        return;
    }
    value.value = clamp(value.value, low, high);
}, { immediate: true });

const handleChange = () => {
    emit('change', {
        id: props.slider?.id,
        name: props.slider?.name,
        value: value.value
    });
};
</script>

<style scoped>
.slider::-webkit-slider-thumb {
    appearance: none;
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #9333ea;
    cursor: pointer;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-webkit-slider-thumb:hover {
    background: #7e22ce;
}

.slider::-moz-range-thumb {
    width: 20px;
    height: 20px;
    border-radius: 50%;
    background: #9333ea;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

.slider::-moz-range-thumb:hover {
    background: #7e22ce;
}
</style>
