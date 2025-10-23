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
      <div
        class="col-span-8 bg-gray-500 rounded-md flex items-center justify-center space-x-3 w-full h-[50vh] relative">
        <div v-if="streamingUrls.stream1 == undefined" class="flex items-center justify-center space-x-3">
          <span class="material-symbols-outlined animate-pulse">
            videocam
          </span>
          <p class="animate-pulse">CAM 01</p>
        </div>
        <iframe v-else :src="streamingUrls.stream1" scrolling="no" class="w-full h-full"></iframe>
        <!-- Leaflet map floating at bottom-left -->
        <div id="drone-fly-map"
          style="position:absolute; left:10px; bottom:16px; width:30%; height:30%; z-index:20; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
        </div>
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
import L from 'leaflet';
export default {
  setup() {
    const controllerStore = useControllerStore();
    const streamingBaseUrl = process.env.VUE_APP_STREAMING_URL
    const currentUserIcon = L.icon({
      iconUrl: 'https://cdn-icons-png.flaticon.com/512/17419/17419361.png ',
      iconSize: [32, 32],
      // iconAnchor: [22, 94],
      // popupAnchor: [-3, -76],
    });
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
      isStarted: false,
      leafletMap: null
    }
  },
  async mounted() {
    let res = await this.controllerStore.getAllControllers();
    if (res.status == "success") {
      this.controller = res.data[0]
      // Do not initialize streams here anymore
    }
    // Initialize Leaflet map after DOM is ready
    this.$nextTick(() => {
      if (!this.leafletMap) {
        this.initLeafletMap();
      }
    });
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
    },
    initLeafletMap() {
      if (this.leafletMap) return;
      // Use the custom currentUserIcon for the marker
      const currentUserIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/17419/17419361.png',
        iconSize: [32, 32],
      });
      if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(position => {
          const lat = position.coords.latitude;
          const lng = position.coords.longitude;
          const map = L.map('drone-fly-map', {
            center: [lat, lng],
            zoom: 13,
            zoomControl: false,
            attributionControl: false
          });
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
          }).addTo(map);
          L.marker([lat, lng], { icon: currentUserIcon }).addTo(map)
          this.leafletMap = map;
        }, () => {
          // Fallback to Phnom Penh if geolocation fails
          const map = L.map('leaflet-map', {
            center: [11.5564, 104.9282], // Phnom Penh
            zoom: 13,
            zoomControl: false,
            attributionControl: false
          });
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19
          }).addTo(map);
          this.leafletMap = map;
        });
      } else {
        // Fallback if geolocation not supported
        const map = L.map('leaflet-map', {
          center: [11.5564, 104.9282], // Phnom Penh
          zoom: 13,
          zoomControl: false,
          attributionControl: false
        });
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19
        }).addTo(map);
        this.leafletMap = map;
      }
    }
  }
}
</script>
