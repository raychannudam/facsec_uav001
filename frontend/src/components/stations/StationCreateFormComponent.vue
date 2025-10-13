<template>
    <form class="flex flex-col space-y-3" @key.esc="closeBtnClikced" @submit.prevent="createStation">
        <div class="py-3 border-b flex flex-row space-x-2 items-center">
            <span class="material-symbols-outlined">
                warehouse
            </span>
            <p>Create a New Station</p>
        </div>
        <div class="relative">
            <input type="text" id="name" v-model="name"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="name"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Name *</label>
        </div>
        <div class="relative">
            <input type="text" id="description" v-model="description"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label for="description"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Description</label>
        </div>
        <div class="flex flex-row space-x-2">
            <div class="relative">
                <input type="text" id="latitude" v-model="latitude"
                    class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                    placeholder=" "  required disabled />
                <label for="latitude"
                    class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Latitude *</label>
            </div>
            <div class="relative">
                <input type="text" id="longitude" v-model="longitude"
                    class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                    placeholder=" " required disabled />
                <label for="longitude"
                    class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Longitude *</label>
            </div>
        </div>
        <div class="flex flex-row space-x-3 items-center justify-end">
            <button class=" text-white bg-blue-600 rounded-md">
                <div class="flex flex-row items-center justify-center space-x-2 p-2">
                    <span class="material-symbols-outlined text-xs">
                        add_circle
                    </span>
                    <p>Create new</p>
                </div>
            </button>
            <button class=" text-white bg-red-600 rounded-md" @click="closeBtnClikced">
                <div class="flex flex-row items-center justify-center space-x-2 p-2">
                    <span class="material-symbols-outlined text-xs">
                        cancel
                    </span>
                    <p>Cancel</p>
                </div>
            </button>
        </div>
    </form>
</template>

<script>
import { useAppStore } from '@/stores/AppStore';
import { useStationStore } from '@/stores/StationStore';
export default {
    props: {
        lat: Number,
        long: Number
    },
    setup() {
        const appStore = useAppStore();
        const stationStore = useStationStore();
        return {
            appStore,
            stationStore,
        }
    },
    data() {
        return {
            name: "",
            description: "",
            latitude: this.lat,
            longitude: this.long
        }
    },
    methods: {
        closeBtnClikced() {
            this.$emit("onClose")
        },
        async createStation(){
            this.appStore.displayPageLoading(true);
            let data = {
                'name': this.name,
                'description': this.description,
                'lat': this.lat,
                'long': this.long
            }
            let res = await this.stationStore.createStation(data);
            this.appStore.displayPageLoading(false);
            this.appStore.displayRightToast(res.status, res.message);
            this.resetForm();
            if (res.status == "success"){
                this.$emit("onStationCreate");
            }
        },
        resetForm(){
            this.name = "";
            this.description = "";
        }
    }
}
</script>