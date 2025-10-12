<!-- <template>
    <div class="absolute z-40 text-xs p-3 bg-black/50 rounded-md" v-if="isDisplayButtons"
        :style="{ top: clickedY + 'px', left: clickedX + 'px' }">
        <StationCreateFormComponent @onClose="isDisplayButtons = false" :lat="clickedLatLong.lat"
            :long="clickedLatLong.lng"></StationCreateFormComponent>
    </div>
    <div class="absolute bg-black/70 right-0 m-10 flex flex-col z-40 space-y-3 p-3 text-sm items-start rounded-md">
        <form class="flex items-center max-w-sm mx-auto">
            <label for="simple-search" class="sr-only">Search</label>
            <div class="relative w-full">
                <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <span class="material-symbols-outlined text-sm">
                        warehouse
                    </span>
                </div>
                <input type="text" id="simple-search"
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
        <div class="w-full grid grid-cols-2  gap-3">
            <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
                <span class="material-symbols-outlined text-sm">
                    warehouse
                </span>
                <p>Stations</p>
            </div>
            <div>
                <p class="text-xs">All <span class="block text-xl font-bold">03</span></p>
            </div>
            <div>
                <p class="text-xs">Active<span class="block text-xl font-bold">03</span></p>
            </div>
            <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
                <span class="material-symbols-outlined text-sm">
                    drone
                </span>
                <p>Drones</p>
            </div>
            <div>
                <p class="text-xs">All <span class="block text-xl font-bold">03</span></p>
            </div>
            <div>
                <p class="text-xs">Active<span class="block text-xl font-bold">03</span></p>
            </div>
        </div>
    </div>
    <div id="map" style="height: 85vh;" class="rounded-md z-30"></div>
</template>

<script>
import StationCreateFormComponent from '@/components/stations/StationCreateFormComponent.vue';
import { useAppStore } from '@/stores/AppStore';
import { useStationStore } from '@/stores/StationStore';
import L from 'leaflet';
export default {
    setup(){
        const appStore = useAppStore();
        const stationStore = useStationStore();
        return {
            appStore,
            stationStore,
        }
    },
    components: {
        StationCreateFormComponent
    },
    async mounted() {
        await this.getAllStations();
        this.initMap();
    },
    data() {
        return {
            allStations: [],
            isDisplayButtons: false,
            clickedLatLong: "",
            clickedX: "",
            clickedY: "",
        }
    },
    methods: {
        initMap() {
            if ("geolocation" in navigator) {
                navigator.geolocation.getCurrentPosition((position) => {
                    let currentUserIcon = L.icon({
                        iconUrl: 'https://cdn-icons-png.flaticon.com/512/164/164600.png',
                        iconSize: [30, 30],
                        // iconAnchor: [22, 94],
                        // popupAnchor: [-3, -76],
                    });
                    let stationIcon = L.icon({
                        iconUrl: 'https://cdn-icons-png.flaticon.com/512/1198/1198294.png',
                        iconSize: [30, 30],
                        // iconAnchor: [22, 94],
                        // popupAnchor: [-3, -76],
                    });
                    let popup = L.popup();
                    const map = L.map('map').setView([position.coords.latitude, position.coords.longitude], 16);
                    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    }).addTo(map);
                    L.marker([position.coords.latitude, position.coords.longitude], {
                        icon: currentUserIcon
                    }).addTo(map)
                        .bindPopup('You are here!')
                        .openPopup();

                    if (this.allStations.length > 0){
                        this.allStations.forEach(station=>{
                            L.marker([station.lat, station.long], {
                                icon: stationIcon
                            }).addTo(map).bindPopup(station.name);
                        })
                    }
                    map.on("click", (e) => {
                        this.isDisplayButtons = true;
                        this.clickedLatLong = e.latlng;
                        this.clickedX = e.containerPoint.x;
                        this.clickedY = e.containerPoint.y;
                    })
                });
            }
        },
        async getAllStations(){
            this.appStore.displayPageLoading(true);
            let res = await this.stationStore.getAllStations();
            this.appStore.displayPageLoading(false);
            this.appStore.displayRightToast(res.status, res.message);
            if (res.status === "success"){
                this.allStations = res.data
            }
        }
    },

}

</script> -->

<template>
  <!-- Form popup on map click -->
  <div
    class="absolute z-40 text-xs p-3 bg-black/50 rounded-md"
    v-if="isDisplayButtons"
    :style="{ top: clickedY + 'px', left: clickedX + 'px' }"
  >
    <StationCreateFormComponent
      @onClose="isDisplayButtons = false"
      @onStationCreate="handleStationCreated"
      :lat="clickedLatLong.lat"
      :long="clickedLatLong.lng"
    />
  </div>

  <!-- Sidebar UI -->
  <div class="absolute bg-black/70 right-0 m-10 flex flex-col z-40 space-y-3 p-3 text-sm items-start rounded-md">
    <form class="flex items-center max-w-sm mx-auto">
      <label for="simple-search" class="sr-only">Search</label>
      <div class="relative w-full">
        <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
          <span class="material-symbols-outlined text-sm">warehouse</span>
        </div>
        <input
          type="text"
          id="simple-search"
          class="bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full ps-10 p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
          placeholder="Search station name..."
          required
        />
      </div>
      <button
        type="submit"
        class="p-2.5 ms-2 text-sm font-medium text-white bg-blue-700 rounded-lg border border-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800"
      >
        <svg class="w-4 h-4" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
          <path
            stroke="currentColor"
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z"
          />
        </svg>
        <span class="sr-only">Search</span>
      </button>
    </form>

    <!-- Stats -->
    <div class="w-full grid grid-cols-2 gap-3">
      <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
        <span class="material-symbols-outlined text-sm">warehouse</span>
        <p>Stations</p>
      </div>
      <div>
        <p class="text-xs">All <span class="block text-xl font-bold">03</span></p>
      </div>
      <div>
        <p class="text-xs">Active<span class="block text-xl font-bold">03</span></p>
      </div>
      <div class="flex items-center space-x-1 text-sm col-span-2 border-b">
        <span class="material-symbols-outlined text-sm">drone</span>
        <p>Drones</p>
      </div>
      <div>
        <p class="text-xs">All <span class="block text-xl font-bold">03</span></p>
      </div>
      <div>
        <p class="text-xs">Active<span class="block text-xl font-bold">03</span></p>
      </div>
    </div>
  </div>

  <!-- Map -->
  <div id="map" style="height: 85vh;" class="rounded-md z-30"></div>
</template>

<script>
import L from 'leaflet';
import StationCreateFormComponent from '@/components/stations/StationCreateFormComponent.vue';
import { useAppStore } from '@/stores/AppStore';
import { useStationStore } from '@/stores/StationStore';

export default {
  components: {
    StationCreateFormComponent,
  },
  data() {
    return {
      map: null,
      stationMarkers: [],
      allStations: [],
      isDisplayButtons: false,
      clickedLatLong: "",
      clickedX: "",
      clickedY: "",
    };
  },
  setup() {
    const appStore = useAppStore();
    const stationStore = useStationStore();
    return {
      appStore,
      stationStore,
    };
  },
  async mounted() {
    await this.getAllStations();
    this.initMap();
  },
  methods: {
    async getAllStations() {
      this.appStore.displayPageLoading(true);
      const res = await this.stationStore.getAllStations();
      this.appStore.displayPageLoading(false);
      this.appStore.displayRightToast(res.status, res.message);
      if (res.status === 'success') {
        this.allStations = res.data;
      }
    },

    initMap() {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          const currentUserIcon = L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/164/164600.png',
            iconSize: [30, 30],
          });

          const stationIcon = L.icon({
            iconUrl: 'https://cdn-icons-png.flaticon.com/512/1198/1198294.png',
            iconSize: [30, 30],
          });

          this.map = L.map('map').setView([position.coords.latitude, position.coords.longitude], 16);

          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; OpenStreetMap contributors',
          }).addTo(this.map);

          // User marker
          L.marker([position.coords.latitude, position.coords.longitude], {
            icon: currentUserIcon,
          })
            .addTo(this.map)
            .bindPopup('You are here!')
            .openPopup();

          // Add existing station markers
          this.addStationMarkers();

          // Handle map click
          this.map.on("click", (e) => {
            this.isDisplayButtons = true;
            this.clickedLatLong = e.latlng;
            this.clickedX = e.containerPoint.x;
            this.clickedY = e.containerPoint.y;
          });
        });
      }
    },

    addStationMarkers() {
      const stationIcon = L.icon({
        iconUrl: 'https://cdn-icons-png.flaticon.com/512/1198/1198294.png',
        iconSize: [30, 30],
      });

      this.allStations.forEach((station) => {
        const marker = L.marker([station.lat, station.long], { icon: stationIcon })
          .addTo(this.map)
          .bindPopup(station.name);
        this.stationMarkers.push(marker);
      });
    },

    async reloadStations() {
      // Clear old station markers
      this.stationMarkers.forEach((marker) => {
        this.map.removeLayer(marker);
      });
      this.stationMarkers = [];

      // Reload station data and re-add markers
      await this.getAllStations();
      this.addStationMarkers();
    },

    async handleStationCreated() {
      this.isDisplayButtons = false;
      await this.reloadStations();
    },
  },
};
</script>

<style scoped>
/* Add any custom styles if needed */
</style>
