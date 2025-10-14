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
            :lat="clickedLatLong.lat" :long="clickedLatLong.lng"></StationCreateFormComponent>
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
              <button v-for="data in foundStationsByQuery"
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
                    v-if="allStations.length < 10">0</span>{{
                      allStations.length }}</span></p>
            </div>
            <div>
              <p class="text-xs">Active<span class="block text-xl font-bold"><span
                    v-if="allStations.length < 10">0</span>{{
                      allStations.length }}</span></p>
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
        <div id="map" style="height: 50vh;" class="rounded-md z-30"></div>
      </div>
    </div>
  </div>

</template>

<script>
import StationCreateFormComponent from '@/components/stations/StationCreateFormComponent.vue';
import { useAppStore } from '@/stores/AppStore';
import { useStationStore } from '@/stores/StationStore';
// import L from 'leaflet';
export default {
  setup() {
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
      isCreatingStation: false,
      clickedLatLong: "",
      map: undefined,
      searchStationQuery: "",
      foundStationsByQuery: [],
      selectedStation: undefined,
    }
  },
  methods: {
    initMap(lat = undefined, lng = undefined) {
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
          if (lat == undefined || lng == undefined) {
            this.map = L.map('map').setView([position.coords.latitude, position.coords.longitude], 16);
          } else {
            this.map = L.map('map').setView([lat, lng], 16);
          }
          L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          }).addTo(this.map);
          L.marker([position.coords.latitude, position.coords.longitude], {
            icon: currentUserIcon
          }).addTo(this.map)
            .bindPopup('You are here!')
            .openPopup();

          if (this.allStations.length > 0) {
            this.allStations.forEach(station => {
              L.marker([station.lat, station.long], {
                icon: stationIcon
              }).addTo(this.map).on('click', () => {
                L.popup().setLatLng([station.lat, station.long]).setContent(`${station.name}`).openOn(this.map)
              });
            })
          }

          L.Control.geocoder({
            position: "topleft",
            defaultMarkGeocode: true // adds a marker when found
          }).addTo(this.map);

          this.map.on("click", (e) => {
            this.isCreatingStation = true;
            this.clickedLatLong = e.latlng;
            // this.map.off();
            // this.map.remove();
            // this.initMap(this.clickedLatLong.lat, this.clickedLatLong.lng);
          })
        });
      }
    },
    async getAllStations() {
      this.appStore.displayPageLoading(true);
      let res = await this.stationStore.getAllStations();
      this.appStore.displayPageLoading(false);
      this.appStore.displayRightToast(res.status, res.message);
      this.allStations = res.data
      if (res.status == "success") {
        this.allStations = res.data
      }
    },
    async searchStation() {
      if (this.searchStationQuery != "") {
        let res = await this.stationStore.getAllStations(this.searchStationQuery);
        if (res.status == "success") {
          this.foundStationsByQuery = res.data;
        } else {
          this.foundStationsByQuery = [];
        }
      } else {
        this.foundStationsByQuery = [];
      }
    },
    async selectStation(stationData) {
      this.selectedStation = stationData
      this.map.flyTo([stationData.lat, stationData.long], 16, {
        animate: true,
        duration: 0.5
      })
      this.map.once('moveend', () => {
        L.popup()
          .setLatLng([stationData.lat, stationData.long])
          .setContent(`${stationData.name}`)
          .openOn(this.map);
      });
      this.foundStationsByQuery = ""
      this.searchStationQuery = ""
    },
    async stationCreateFormClosed() {
      this.isCreatingStation = false
    },
    async stationCreateFormSubmited() {
      this.isCreatingStation = false
      await this.getAllStations();
      this.map.off();
      this.map.remove();
      this.initMap(this.clickedLatLong.lat, this.clickedLatLong.lng);
    },
    moveToMyLocation() {
      if ("geolocation" in navigator) {
        navigator.geolocation.getCurrentPosition((position) => {
          this.map.flyTo([position.coords.latitude, position.coords.longitude], 16, {
            animate: true,
            duration: 0.5
          })
        })
      }
    }
  },
}

</script>

<style>
/* Change search box text color to black */
.leaflet-control-geocoder-form input {
  color: black !important;
}

/* Optional: change placeholder color too */
.leaflet-control-geocoder-form input::placeholder {
  color: #555 !important;
}
</style>