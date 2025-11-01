<template>
  <div class="flex flex-col space-y-3">
    <div class="flex flex-col space-y-3">
      <div class="text-2xl font-bold flex items-center space-x-3">
        <span class="text-2xl material-symbols-outlined">
          warehouse
        </span>
        <p>Drone Stations</p>
      </div>
      <p class="text-gray-600 dark:text-gray-400">Manage your drone stations on the map directly.</p>
      <hr class="border-0.5 border-gray-200">
      <div class="relative">
        <div @click.self="stationCreateFormClosed"
          class="absolute z-40 text-xs bg-black/80 w-full h-full rounded-md flex items-center justify-center"
          v-if="isCreatingStation">
          <StationCreateFormComponent @onClose="stationCreateFormClosed" @onStationCreate="stationCreateFormSubmited"
            :lat="clickedLatLong.lat" :long="clickedLatLong.lng">
          </StationCreateFormComponent>
        </div>
        <button @click="moveToMyLocation"
          class="absolute dark:bg-black/70 bg-white/70 bottom-0 left-0 m-10 flex flex-col z-40 space-y-3 p-3 text-sm items-start rounded-full">
          <span class="material-symbols-outlined">
            my_location
          </span>
        </button>
        <div
          class="absolute dark:bg-black/70 bg-white/70 right-0 m-10 flex flex-col z-40 space-y-3 p-3 text-sm items-start rounded-md">
          <div class="relative flex flex-col space-y-3">
            <form class="flex items-center max-w-sm mx-auto" @submit.prevent="searchStation">
              <label for="searchStationQuery" class="sr-only">Search</label>
              <div class="relative w-full">
                <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                  <span class="material-symbols-outlined text-sm">
                    warehouse
                  </span>
                </div>
                <input type="text" id="searchStationQuery" v-model="searchStationQuery" @input="searchStation"
                  class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                  placeholder="Search station name..." required />
              </div>
              <button type="submit"
                class="p-2.5 ms-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                  viewBox="0 0 20 20">
                  <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                </svg>
                <span class="sr-only">Search</span>
              </button>
            </form>
            <div class="absolute top-9 w-full p-3 rounded-md bg-white/80 text-gray-700 flex flex-col space-y-1"
              v-if="foundStationsByQuery.length > 0">
              <button v-for="data in foundStationsByQuery" :key="data.id"
                class="border-b border-gray-900 text-xs text-start p-2 hover:bg-gray-900 hover:text-white text-gray-700 rounded-md"
                @click="selectStation(data)">
                {{ data.name }}
              </button>
            </div>
          </div>
          <div class="w-full grid grid-cols-2  gap-3">
            <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
              <span class="material-symbols-outlined text-sm">
                warehouse
              </span>
              <p>Stations</p>
            </div>
            <div>
              <p class="text-xs">All <span class="block text-xl font-bold"><span
                    v-if="allStations.length < 10">0</span>{{ allStations.length }}</span></p>
            </div>
            <div>
              <p class="text-xs">Active<span class="block text-xl font-bold"><span
                    v-if="allStations.length < 10">0</span>{{ allStations.length }}</span></p>
            </div>
            <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
              <span class="material-symbols-outlined text-sm">
                drone
              </span>
              <p>Drones</p>
            </div>
            <div>
              <p class="text-xs">All <span class="block text-xl font-bold">00</span></p>
            </div>
            <div>
              <p class="text-xs">Active<span class="block text-xl font-bold">00</span></p>
            </div>
          </div>
        </div>
        <div id="map" style="height: 55vh;" class="rounded-md z-30"></div>
      </div>
    </div>
    <div>
      <StationDetailView :station-data="clickedStation"></StationDetailView>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import StationCreateFormComponent from '@/components/stations/StationCreateFormComponent.vue';
import StationDetailView from './StationDetailView.vue';
import { useAppStore } from '@/stores/AppStore';
import { useStationStore } from '@/stores/StationStore';
import L from 'leaflet';

// Stores
const appStore = useAppStore();
const stationStore = useStationStore();

// Reactive state
const allStations = ref([]);
const isCreatingStation = ref(false);
const clickedLatLong = ref("");
const map = ref(undefined);
const searchStationQuery = ref("");
const foundStationsByQuery = ref([]);
const selectedStation = ref(undefined);
const clickedStation = ref(undefined);

// Icon definitions
const currentUserIcon = L.icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/17419/17419361.png',
  iconSize: [32, 32],
});

const stationIcon = L.icon({
  iconUrl: 'https://cdn-icons-png.flaticon.com/512/1188/1188034.png',
  iconSize: [35, 35],
});

// Methods
const initMap = (lat = undefined, lng = undefined) => {
  if (map.value) return;

  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition((position) => {
      const mapCenter = (lat !== undefined && lng !== undefined)
        ? [lat, lng]
        : [position.coords.latitude, position.coords.longitude];

      map.value = L.map('map').setView(mapCenter, 16);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(map.value);

      L.marker([position.coords.latitude, position.coords.longitude], {
        icon: currentUserIcon
      }).addTo(map.value);

      if (allStations.value.length > 0) {
        allStations.value.forEach(station => {
          L.marker([station.lat, station.long], {
            icon: stationIcon
          }).addTo(map.value).on("click", () => {
            clickedStation.value = station;
          });
        });
      }

      map.value.on("click", (e) => {
        isCreatingStation.value = true;
        clickedLatLong.value = e.latlng;
      });
    });
  }
};

const getAllStations = async () => {
  appStore.displayPageLoading(true);
  const res = await stationStore.getAllStations();
  appStore.displayPageLoading(false);
  appStore.displayRightToast(res.status, res.message);

  if (res.status === "success") {
    allStations.value = res.data;
  }
};

const searchStation = async () => {
  if (searchStationQuery.value !== "") {
    const res = await stationStore.getAllStations(searchStationQuery.value);
    foundStationsByQuery.value = res.status === "success" ? res.data : [];
  } else {
    foundStationsByQuery.value = [];
  }
};

const selectStation = async (stationData) => {
  selectedStation.value = stationData;
  map.value.flyTo([stationData.lat, stationData.long], 16, {
    animate: true,
    duration: 0.5
  });
  foundStationsByQuery.value = [];
  searchStationQuery.value = "";
};

const stationCreateFormClosed = () => {
  isCreatingStation.value = false;
};

const stationCreateFormSubmited = async () => {
  isCreatingStation.value = false;
  await getAllStations();

  if (map.value && clickedLatLong.value) {
    const newStation = allStations.value && allStations.value.length > 0
      ? allStations.value[allStations.value.length - 1]
      : null;

    L.marker([
      clickedLatLong.value.lat,
      clickedLatLong.value.lng
    ], {
      icon: stationIcon
    }).addTo(map.value).on("click", () => {
      clickedStation.value = newStation;
    });
  }
};

const moveToMyLocation = () => {
  if ("geolocation" in navigator) {
    navigator.geolocation.getCurrentPosition((position) => {
      map.value.flyTo([position.coords.latitude, position.coords.longitude], 16, {
        animate: true,
        duration: 0.5
      });
    });
  }
};

// Lifecycle
onMounted(async () => {
  document.title = "All Stations | DRSYS";
  await getAllStations();
  initMap();
});
</script>