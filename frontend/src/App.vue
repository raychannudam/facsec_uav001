<template>
  <div v-if="windowWidth >= 1000" class="p-3 dark:bg-gray-900 min-h-screen flex flex-col dark:text-gray-100 text-gray-900">
    <router-view></router-view>
  </div>
  <div v-else class="flex flex-col items-center justify-center min-h-screen w-screen bg-gray-100 dark:bg-gray-900">
    <span class="dark:text-white material-symbols-outlined text-6xl">
      fit_screen
    </span>
    <h1 class="text-2xl font-bold mb-4 text-gray-800 dark:text-gray-200">Screen Too Small</h1>
    <p class="text-gray-600 dark:text-gray-400 text-center w-full">Please use a device with a larger screen to access this application.</p>
  </div>
<PageLoadingComponent></PageLoadingComponent>
<RightToastComponent :status="appStore.rightToastStatus" :message="appStore.rightToastMessage"></RightToastComponent>

</template>

<style>
.material-symbols-outlined {
  font-variation-settings:
    'FILL' 0,
    'wght' 400,
    'GRAD' 0,
    'opsz' 24
}
</style>

<script>
import { initFlowbite } from 'flowbite'
import PageLoadingComponent from './components/utils/PageLoadingComponent.vue';
import RightToastComponent from './components/utils/RightToastComponent.vue';
import { useAppStore } from '@/stores/AppStore';
export default {
  setup() {
    const appStore = useAppStore();
    return {
      appStore
    }
  },
  name: 'App',
  components: {
    PageLoadingComponent,
    RightToastComponent,
  },
  data() {
    return {
      windowWidth: window.innerWidth,
      windowHeight: window.innerHeight
    }
  },
  async mounted() {
    initFlowbite();
    window.addEventListener('resize', this.updateWindowDimensions);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.updateWindowDimensions);
  },
  methods: {
    updateWindowDimensions() {
      this.windowWidth = window.innerWidth;
      this.windowHeight = window.innerHeight;
    }
  },
};
</script>
