<template>
    <Teleport to="body">
        <div v-if="isOpen" class="fixed inset-0 z-50 overflow-y-auto" style="background-color: rgba(0, 0, 0, 0.5);">
            <div class="min-h-screen px-4 flex items-center justify-center">
                <div class="bg-white dark:bg-gray-800 rounded-lg shadow-xl max-w-md w-full overflow-hidden">
                    <!-- Header -->
                    <div class="bg-red-50 dark:bg-red-900/20 px-6 py-4 border-b border-red-200 dark:border-red-800">
                        <div class="flex items-center gap-3">
                            <div
                                class="flex-shrink-0 w-10 h-10 bg-red-100 dark:bg-red-900/50 rounded-full flex items-center justify-center">
                                <svg class="w-6 h-6 text-red-600 dark:text-red-400" fill="none" stroke="currentColor"
                                    viewBox="0 0 24 24">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                                </svg>
                            </div>
                            <div>
                                <h3 class="text-lg font-bold text-gray-900 dark:text-white">
                                    Confirm Deletion
                                </h3>
                                <p class="text-sm text-gray-600 dark:text-gray-400">
                                    This action cannot be undone
                                </p>
                            </div>
                        </div>
                    </div>

                    <!-- Body -->
                    <div class="p-6">
                        <p class="text-gray-700 dark:text-gray-300 mb-12">
                            {{ message || 'Are you sure you want to delete this item?' }}
                        </p>

                        <div class="flex gap-3">
                            <button type="button" @click="handleDelete"
                                class="flex-1 px-4 py-2.5 text-sm font-medium text-white bg-red-600 hover:bg-red-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-red-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                                Delete
                            </button>
                            <button type="button" @click="$emit('close')"
                                class="flex-1 px-4 py-2.5 text-sm font-medium text-gray-700 dark:text-gray-300 bg-white dark:bg-gray-700 border border-gray-300 dark:border-gray-600 rounded-lg hover:bg-gray-50 dark:hover:bg-gray-600 focus:outline-none focus:ring-2 focus:ring-gray-300 dark:focus:ring-gray-500 transition-colors">
                                Cancel
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </Teleport>
</template>

<script setup>
import { ref, watch, onBeforeUnmount } from 'vue'

const props = defineProps({
    isOpen: {
        type: Boolean,
        default: false
    },
    message: {
        type: String,
        default: ''
    },
    drone: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['close', 'confirm'])

// Lock body scroll when modal opens
watch(
    () => props.isOpen,
    (isOpen) => {
        if (isOpen) {
            const scrollY = window.scrollY
            document.body.style.position = 'fixed'
            document.body.style.top = `-${scrollY}px`
            document.body.style.width = '100%'
        } else {
            const scrollY = document.body.style.top
            document.body.style.position = ''
            document.body.style.top = ''
            document.body.style.width = ''
            window.scrollTo(0, parseInt(scrollY || '0') * -1)
        }
    },
    { immediate: true }
)

onBeforeUnmount(() => {
    document.body.style.position = ''
    document.body.style.top = ''
    document.body.style.width = ''
})

const handleDelete = () => {
    if (!props.drone || !props.drone.id) return
    emit('confirm', props.drone.id)
}
</script>
