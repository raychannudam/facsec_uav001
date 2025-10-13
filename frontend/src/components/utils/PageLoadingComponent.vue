<template>
  <div
    class="z-50 flex items-center justify-center w-screen h-screen bg-black/80 fixed top-0 left-0"
    v-if="isVisible"
  >
    <div
      class="px-3 py-1 text-xs font-medium leading-none text-center text-blue-800 bg-blue-200 rounded-full animate-pulse dark:bg-blue-900 dark:text-blue-200"
    >
      loading...
    </div>
  </div>
</template>

<script>
import { useAppStore } from "@/stores/AppStore";
import { initFlowbite } from "flowbite";
import { storeToRefs } from "pinia";
export default {
  setup() {
    const appStore = useAppStore();
    const { isPageLoading } = storeToRefs(appStore);
    return {
      appStore,
      isPageLoading,
    };
  },
  data() {
    return {
      isVisible: false,
    };
  },
  mounted() {
    initFlowbite();
  },
  watch: {
    isPageLoading: {
      handler(newVal, oldVal) {
        this.isVisible = newVal;
      },
    },
  },
};
</script>
