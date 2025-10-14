<template>
    <div class="flex flex-col space-y-3">
        <div class="text-2xl font-bold flex items-center space-x-3">
            <span class="text-2xl material-symbols-outlined">
                settings_input_component
            </span>
            <p>Configuration</p>
        </div>
        <p class="text-gray-600 dark:text-gray-400">Manage your control panel.</p>
        <hr class="border-0.5 border-gray-200">
        <div class="flex flex-col space-y-3">
            <!-- Select UAV -->
            <div class="flex flex-row space-x-3 items-center justify-start">
                <p class="text-sm font-bold">Selected UAV</p>
                <button id="selectDroneDropdownSearchButton" data-dropdown-toggle="selectDroneDropdownSearch"
                    data-dropdown-placement="bottom"
                    class="text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center   dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
                    type="button">Please select a UAV <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true"
                        xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="m1 1 4 4 4-4" />
                    </svg>
                </button>
                <!-- Dropdown menu -->
                <div id="selectDroneDropdownSearch"
                    class="z-10 hidden bg-white rounded-lg shadow-sm w-60 dark:bg-gray-700">
                    <div class="p-3">
                        <label for="droneSearchQuery" class="sr-only">Search</label>
                        <div class="relative">
                            <div
                                class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
                                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                                </svg>
                            </div>
                            <input type="text" id="droneSearchQuery" v-model="droneSearchQuery"
                                class="block w-full p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Search drone name...">
                        </div>
                    </div>
                    <ul class="h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-700 dark:text-gray-200"
                        aria-labelledby="selectDroneDropdownSearchButton">
                        <li>
                            <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input id="checkbox-item-11" type="radio" value="1" v-model="selectedDrone"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                                <label for="checkbox-item-11"
                                    class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">Bonnie
                                    Green</label>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="flex items-center justify-center">
                <img src="https://img1.wsimg.com/isteam/ip/c1baed06-ecd8-44e0-9dd4-c41e78892caf/agribot-drone-iotech-world-m3.png"
                    class="h-40" alt="">
            </div>
        </div>
    </div>
</template>
<script>
import { useDroneStore } from '@/stores/droneStore';
import { useAppStore } from '@/stores/AppStore';
export default {
    setup() {
        const droneStore = useDroneStore();
        const appStore = useAppStore();
        return {
            droneStore,
            appStore
        }
    },
    data() {
        return {
            allDrones: undefined,
            droneSearchQuery: "",
            selectedDrone: undefined
        }
    },
    async mounted() {

    },
    methods: {
        async getAllDrones() {
        }
    }

}
</script>