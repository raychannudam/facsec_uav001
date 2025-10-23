<template>
  <div class="flex flex-col space-y-3">
    <div class="flex flex-row space-x-3 items-center">
      <div class="text-2xl font-bold flex items-center space-x-3">
        <span class="text-2xl material-symbols-outlined">
          camera_video
        </span>
        <p>Live Streams</p>
      </div>
      <button @click="startStream" :disabled="isStarted == true"
        class="flex flex-row space-x-2 text-sm py-1 items-center px-4 hover:bg-blue-500 rounded-full border-blue-500 border focus:ring-blue-800 focus:ring-4">
        <span class="material-symbols-outlined text-sm">
          play_arrow
        </span>
        <p>Start Now</p>
      </button>
      <button @click="restartStream"
        class="flex flex-row space-x-2 text-sm py-1 items-center px-4 hover:bg-red-500 rounded-full border-red-500 border focus:ring-red-800 focus:ring-4">
        <span class="material-symbols-outlined text-sm">
          restart_alt
        </span>
        <p>Restart</p>
      </button>
    </div>
    <p class="text-gray-600 dark:text-gray-400">Get real-time live stream video from the cameras on the
      drone.</p>
    <hr class="border-0.5 border-gray-200">
    <div class="grid grid-cols-12 gap-3">
      <div class="col-span-8 bg-gray-500 rounded-md flex items-center justify-center space-x-3 w-full h-[50vh]">
        <div v-if="streamingUrls.stream1 == undefined" class="flex items-center justify-center space-x-3">
          <span class="material-symbols-outlined animate-pulse">
            videocam
          </span>
          <p class="animate-pulse">CAM 01</p>
        </div>
        <iframe v-else :src="streamingUrls.stream1" scrolling="no" class="w-full h-full"></iframe>
      </div>
      <div class="col-span-4 h-[50vh]">
        <div class="grid grid-rows-3 gap-3 w-full h-full">
          <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 overflow-clip w-full h-full">
            <div v-if="streamingUrls.stream2 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">
                videocam
              </span>
              <p class="animate-pulse">CAM 02</p>
            </div>
            <iframe v-else :src="streamingUrls.stream2" scrolling="yes" class="w-full h-full"></iframe>
          </div>
          <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 ">
            <div v-if="streamingUrls.stream3 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">
                videocam
              </span>
              <p class="animate-pulse">CAM 03 {{ streamingUrls.stream3 }}</p>
            </div>
            <iframe v-else :src="streamingUrls.stream3" scrolling="yes" class="w-full h-full"></iframe>
          </div>
          <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 ">
            <div v-if="streamingUrls.stream4 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">
                videocam
              </span>
              <p class="animate-pulse">CAM 04</p>
            </div>
            <iframe v-else :src="streamingUrls.stream4" scrolling="yes" class="w-full h-full"></iframe>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { useControllerStore } from '@/stores/ControllerStore';
export default {
  setup() {
    const controllerStore = useControllerStore();
    const streamingBaseUrl = process.env.VUE_APP_STREAMING_URL
    return {
      controllerStore,
      streamingBaseUrl
    }
  },
  data() {
    return {
      streamingUrls: {
        stream1: undefined,
        stream2: undefined,
        stream3: undefined,
        stream4: undefined
      },
      controller: undefined,
      username: '',
      password: '',
      isStarted: false
    }
  },
  async mounted() {
    let res = await this.controllerStore.getAllControllers();
    if (res.status == "success") {
      this.controller = res.data[0]
      // Do not initialize streams here anymore
    }
  },
  methods: {
    async startStream() {
      if (!this.isStarted) {
        const hasSelectedUrl = ["stream1", "stream2", "stream3", "stream4"].some(
          id => {
            const stream = this.controller.config.streamingUrls.find(item => item.id == id);
            return stream && stream.selectedUrl && Object.keys(stream.selectedUrl).length > 0;
          }
        );
        if (hasSelectedUrl) {
          this.username = prompt("Streaming client username:", "username");
          if (this.username == null) return;
          this.password = prompt("Streaming client password", "password");
          if (this.password == null) return;
        }
        ["stream1", "stream2", "stream3", "stream4"].forEach(id => {
          const stream = this.controller.config.streamingUrls.find(item => item.id == id);
          if (stream && stream.selectedUrl && Object.keys(stream.selectedUrl).length > 0) {
            this.streamingUrls[id] = this.streamingBaseUrl + "/" + stream.selectedUrl.name + `?username=${this.username}&password=${this.password}`;
          }
        });
        this.isStarted = true

      }
    },
    restartStream() {
      if (this.isStarted) {
        ["stream1", "stream2", "stream3", "stream4"].forEach(id => {
          const stream = this.controller.config.streamingUrls.find(item => item.id == id);
          if (stream && stream.selectedUrl && Object.keys(stream.selectedUrl).length > 0) {
            this.streamingUrls[id] = this.streamingBaseUrl + "/" + stream.selectedUrl.name + `?username=${this.username}&password=${this.password}`;
          }
        });
      }
    }
  }
}
</script>
