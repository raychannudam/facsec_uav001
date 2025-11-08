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
          style="position:absolute; left:10px; bottom:16px; width:25%; height:20%; z-index:20; border-radius:8px; overflow:hidden; box-shadow:0 2px 8px rgba(0,0,0,0.2);">
        </div>

        <!-- Drone info overlay -->
        <div v-if="droneLocation"
          style="position:absolute; left:10px; top:16px; z-index:20; background:rgba(0,0,0,0.7); padding:8px 12px; border-radius:8px; color:white; font-size:12px;">
          <div><strong>🚁 {{ droneLocation.droneId }}</strong></div>
          <div v-if="droneLocation.altitude">Alt: {{ droneLocation.altitude }}m</div>
          <div v-if="droneLocation.battery">Battery: {{ droneLocation.battery }}%</div>
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
              <p class="animate-pulse">CAM 03</p>
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

<script setup>
import { ref, watch, onMounted, onBeforeUnmount, nextTick } from 'vue';
import { useControllerStore } from '@/stores/ControllerStore';
import L from 'leaflet';

// Props
const props = defineProps({
  droneLocation: {
    type: Object,
    default: null
  }
});

const controllerStore = useControllerStore();
const streamingBaseUrl = process.env.VUE_APP_STREAMING_URL;

const streamingUrls = ref({
  stream1: undefined,
  stream2: undefined,
  stream3: undefined,
  stream4: undefined
});

const controller = ref(undefined);
const username = ref('');
const password = ref('');
const isStarted = ref(false);
const leafletMap = ref(null);
const droneMarker = ref(null);

// Drone icons
const droneIcon = L.icon({
  iconUrl: 'https://api.iconify.design/mdi/quadcopter.svg?color=%232196f3&width=48&height=48',
  iconSize: [48, 48],
  iconAnchor: [24, 24],
  popupAnchor: [0, -24]
});

// Watch for drone location updates from parent
watch(() => props.droneLocation, (newLocation) => {
  if (newLocation && leafletMap.value) {
    updateDroneOnMap(newLocation);
  }
}, { deep: true });

const updateDroneOnMap = (locationData) => {
  if (!leafletMap.value) return;

  const { lat, lng } = locationData;

  if (droneMarker.value) {
    // Update existing marker
    droneMarker.value.setLatLng([lat, lng]);

    // Smoothly pan map to follow drone
    leafletMap.value.setView([lat, lng], leafletMap.value.getZoom(), {
      animate: true,
      pan: { animate: true, duration: 0.5 }
    });
  } else {
    // Create new marker
    droneMarker.value = L.marker([lat, lng], { icon: droneIcon })
      .addTo(leafletMap.value);

    // Center map on drone
    leafletMap.value.setView([lat, lng], 17);
  }
};

const initLeafletMap = () => {
  if (leafletMap.value) return;

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      const map = L.map('drone-fly-map', {
        center: [lat, lng],
        zoom: 17,
        zoomControl: false,
        attributionControl: false
      });

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19
      }).addTo(map);

      leafletMap.value = map;

      // If drone location already exists, show it
      if (props.droneLocation) {
        updateDroneOnMap(props.droneLocation);
      }
    }, () => {
      // Fallback to Phnom Penh
      initFallbackMap();
    });
  } else {
    initFallbackMap();
  }
};

const initFallbackMap = () => {
  const map = L.map('drone-fly-map', {
    center: [11.5564, 104.9282], // Phnom Penh
    zoom: 13,
    zoomControl: false,
    attributionControl: false
  });

  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
  }).addTo(map);

  leafletMap.value = map;

  if (props.droneLocation) {
    updateDroneOnMap(props.droneLocation);
  }
};

const startStream = async () => {
  if (!isStarted.value) {
    const hasSelectedUrl = ["stream1", "stream2", "stream3", "stream4"].some(
      id => {
        const stream = controller.value.config.streamingUrls.find(item => item.id == id);
        return stream && stream.selectedUrl && Object.keys(stream.selectedUrl).length > 0;
      }
    );

    if (hasSelectedUrl) {
      username.value = prompt("Streaming client username", "username");
      if (username.value == null) return;
      password.value = prompt("Streaming client password", "password");
      if (password.value == null) return;
    }

    ["stream1", "stream2", "stream3", "stream4"].forEach(id => {
      const stream = controller.value.config.streamingUrls.find(item => item.id == id);
      if (stream && stream.selectedUrl && Object.keys(stream.selectedUrl).length > 0) {
        streamingUrls.value[id] = streamingBaseUrl + "/" + stream.selectedUrl.name + `?username=${username.value}&password=${password.value}`;
      }
    });

    isStarted.value = true;
  }
};

const restartStream = () => {
  isStarted.value = false;
  startStream();
};

onMounted(async () => {
  let res = await controllerStore.getAllControllers();
  if (res.status == "success") {
    controller.value = res.data[0];
  }

  // Initialize map after DOM is ready
  await nextTick();
  initLeafletMap();
});

onBeforeUnmount(() => {
  if (leafletMap.value) {
    leafletMap.value.remove();
    leafletMap.value = null;
  }
});
</script>