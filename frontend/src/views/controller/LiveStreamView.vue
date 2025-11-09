<template>
  <div class="flex flex-col space-y-3">
    <div class="flex flex-row space-x-3 items-center">
      <div class="text-2xl font-bold flex items-center space-x-3">
        <span class="text-2xl material-symbols-outlined">camera_video</span>
        <p>Live Streams</p>
      </div>

      <button @click="startStream" :disabled="isStarted == true"
        class="flex flex-row space-x-2 text-sm py-1 items-center px-4 hover:bg-blue-500 rounded-full border-blue-500 border">
        <span class="material-symbols-outlined text-sm">play_arrow</span>
        <p>Start Now</p>
      </button>

      <button @click="restartStream"
        class="flex flex-row space-x-2 text-sm py-1 items-center px-4 hover:bg-red-500 rounded-full border-red-500 border">
        <span class="material-symbols-outlined text-sm">restart_alt</span>
        <p>Restart</p>
      </button>
    </div>

    <p class="text-gray-600 dark:text-gray-400">
      Get real-time live stream video from the cameras on the drone.
    </p>
    <hr class="border-0.5 border-gray-200" />

    <div class="grid grid-cols-12 gap-3">
      <div class="col-span-8 bg-gray-500 rounded-md w-full h-[60vh] relative overflow-hidden">

        <div v-if="streamingUrls.stream1 == undefined" class="flex items-center justify-center h-full space-x-3">
          <span class="material-symbols-outlined animate-pulse">videocam</span>
          <p class="animate-pulse">CAM 01</p>
        </div>

        <iframe v-else :src="streamingUrls.stream1" scrolling="no" class="w-full h-full"></iframe>

        <!-- Map enlarged -->
        <div id="drone-fly-map" class="absolute left-3 bottom-3 rounded-md shadow-lg"
          style="width: 35%; height: 28%; z-index: 20; overflow: hidden;"></div>

        <!-- Drone info -->
        <div v-if="droneLocation"
          class="absolute left-3 top-3 bg-black bg-opacity-70 text-white px-3 py-2 rounded-md text-xs z-index-20">

          <div class="flex items-center gap-1">
            <img src="https://cdn-icons-png.flaticon.com/512/4056/4056808.png" alt="drone icon" class="w-4 h-4" />
            <strong>{{ droneLocation.droneId }}</strong>
          </div>

          <div v-if="droneLocation.altitude">Alt: {{ droneLocation.altitude }}m</div>
          <div v-if="droneLocation.battery">Battery: {{ droneLocation.battery }}%</div>
        </div>

      </div>

      <div class="col-span-4 h-[60vh]">
        <div class="grid grid-rows-3 gap-3 w-full h-full">
          <div class="bg-gray-500 rounded-md flex items-center justify-center overflow-hidden">
            <div v-if="streamingUrls.stream2 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">videocam</span>
              <p class="animate-pulse">CAM 02</p>
            </div>
            <iframe v-else :src="streamingUrls.stream2" class="w-full h-full"></iframe>
          </div>
          <div class="bg-gray-500 rounded-md flex items-center justify-center overflow-hidden">
            <div v-if="streamingUrls.stream3 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">videocam</span>
              <p class="animate-pulse">CAM 03</p>
            </div>
            <iframe v-else :src="streamingUrls.stream3" class="w-full h-full"></iframe>
          </div>
          <div class="bg-gray-500 rounded-md flex items-center justify-center overflow-hidden">
            <div v-if="streamingUrls.stream4 == undefined" class="flex items-center justify-center space-x-3">
              <span class="material-symbols-outlined animate-pulse">videocam</span>
              <p class="animate-pulse">CAM 04</p>
            </div>
            <iframe v-else :src="streamingUrls.stream4" class="w-full h-full"></iframe>
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

const props = defineProps({
  droneLocation: Object
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

const droneIcon = L.divIcon({
  className: '',
  html: `
    <div class="drone-icon-inner">
      <img src="https://cdn-icons-png.flaticon.com/512/4056/4056808.png" />
    </div>
  `,
  iconSize: [48, 48],
  iconAnchor: [24, 24]
});

watch(() => props.droneLocation, (loc) => {
  if (loc && leafletMap.value) updateDroneOnMap(loc);
}, { deep: true });

const updateDroneOnMap = (loc) => {
  if (!leafletMap.value) return;
  const { lat, lng } = loc;

  if (!droneMarker.value) {
    droneMarker.value = L.marker([lat, lng], { icon: droneIcon }).addTo(leafletMap.value);
    leafletMap.value.setView([lat, lng], leafletMap.value.getZoom(), { animate: true });
  } else {
    droneMarker.value.setLatLng([lat, lng]);
  }

  leafletMap.value.setView([lat, lng], leafletMap.value.getZoom(), {
    animate: true,
    pan: { animate: true, duration: 0.5 }
  });
};

const initLeafletMap = () => {
  if (leafletMap.value) return;

  const createMap = (lat, lng, zoom = 17) => {
    const map = L.map('drone-fly-map', {
      center: [lat, lng],
      zoom,
      zoomControl: false,
      attributionControl: false
    });

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

    leafletMap.value = map;

    map.on('zoom', () => {
      const z = map.getZoom();
      const scale = Math.max(0.6, z / 17); // prevents icon from shrinking too small
      if (droneMarker.value?._icon) {
        const img = droneMarker.value._icon.querySelector('.drone-icon-inner img');
        if (img) img.style.transform = `scale(${scale})`;
      }
    });

    if (props.droneLocation) updateDroneOnMap(props.droneLocation);
  };

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(
      pos => createMap(pos.coords.latitude, pos.coords.longitude, 17),
      () => createMap(11.5564, 104.9282, 13)
    );
  } else {
    createMap(11.5564, 104.9282, 13);
  }
};

const startStream = async () => {
  if (isStarted.value) return;

  const selectedStreams = ["stream1", "stream2", "stream3", "stream4"];
  const hasSelectedUrl = selectedStreams.some(id => {
    const s = controller.value.config.streamingUrls.find(i => i.id === id);
    return s?.selectedUrl;
  });

  if (hasSelectedUrl) {
    username.value = prompt("Streaming client username", "username");
    if (username.value == null) return;
    password.value = prompt("Streaming client password", "password");
    if (password.value == null) return;
  }

  selectedStreams.forEach(id => {
    const stream = controller.value.config.streamingUrls.find(i => i.id === id);
    if (stream?.selectedUrl) {
      streamingUrls.value[id] = `${streamingBaseUrl}/${stream.selectedUrl.name}?username=${username.value}&password=${password.value}`;
    }
  });

  isStarted.value = true;
};

const restartStream = () => {
  isStarted.value = false;
  startStream();
};

onMounted(async () => {
  const res = await controllerStore.getAllControllers();
  if (res.status === "success") controller.value = res.data[0];

  await nextTick();
  initLeafletMap();
});

onBeforeUnmount(() => {
  leafletMap.value?.remove();
  leafletMap.value = null;
});
</script>

<style>
.drone-icon-inner img {
  width: 48px;
  height: 48px;
  transition: transform 0.2s;
  pointer-events: none;
}
</style>
