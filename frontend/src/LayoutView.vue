<template>
    <div class="border-b border-gray-200 dark:border-gray-700 flex items-center justify-between">
        <ul class="flex flex-wrap -mb-px text-sm font-medium text-center text-gray-500 dark:text-gray-400">
            <li class="me-2">
                <router-link :to="{ name: 'controller' }"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        stadia_controller
                    </span>
                    <p>Controller</p>
                </router-link>
            </li>
            <li class="me-2">
                <router-link :to="{ name: 'drones' }"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        drone
                    </span>
                    <p>All Drones</p>
                </router-link>
            </li>
            <li class="me-2">
                <router-link :to="{ name: 'stations' }"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        warehouse
                    </span>
                    <p>All Stations</p>
                </router-link>
            </li>
            <li class="me-2">
                <router-link :to="{ name: 'settings' }"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        settings
                    </span>
                    <p>Settings</p>
                </router-link>
            </li>
            <li class="me-2">
                <router-link :to="{ name: 'account' }"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        account_circle
                    </span>
                    <p>Account</p>
                </router-link>
            </li>
            <li class="me-2">
                <a href="#"
                    class="inline-flex items-center space-x-3 justify-center p-4 border-b-2 border-transparent rounded-t-lg hover:text-gray-600 hover:border-gray-300 dark:hover:text-gray-300 group text-gray-400 cursor-not-allowed dark:text-gray-500"
                    active-class="text-blue-600 border-blue-600 dark:border-blue-500 group"
                    exact-active-class="text-blue-600 border-blue-600 dark:border-blue-500 group">
                    <span class="material-symbols-outlined">
                        help
                    </span>
                    <p>Help</p>
                </a>
            </li>
        </ul>
        <!-- General Info -->
        <div class="flex items-center space-x-3 dark:text-gray-400 px-3">
            <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                <span class="material-symbols-outlined">
                    device_thermostat
                </span>
                <p>Temp, </p>
                <p class="font-bold dark:text-white">-- &#8451;</p>
            </div>
            <div>
                |
            </div>
            <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                <span class="material-symbols-outlined">
                    speed
                </span>
                <p>Speed, </p>
                <p class="font-bold dark:text-white">-- km/h</p>
            </div>
            <div>
                |
            </div>
            <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                <span class="material-symbols-outlined">
                    altitude
                </span>
                <p>Altitude, </p>
                <p class="font-bold dark:text-white">---- m</p>
            </div>
            <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                <span class="material-symbols-outlined">
                    timer
                </span>
                <p>Time, </p>
                <p class="font-bold dark:text-white">-- mn</p>
            </div>
            <div class="cursor-pointer">
                <button @click="displaySignoutPopup" data-modal-target="signout_popup" data-modal-toggle="signout_popup"
                    class="text-xs inline-flex items-center space-x-3 justify-center p-4 group hover:text-gray-600 dark:hover:text-gray-300 group text-gray-400 dark:text-gray-500">
                    <span class="material-symbols-outlined">
                        logout
                    </span>
                    <p>Sign out</p>
                </button>
                <ConfirmPopupModelComponent model_id="signout_popup"></ConfirmPopupModelComponent>
            </div>
        </div>
    </div>
    <div class="p-3 dark:text-white">
        <router-view></router-view>
    </div>
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
import { RouterView } from 'vue-router';
import { useAppStore } from './stores/AppStore';
import { useAuthStore } from './stores/AuthStore';
import { storeToRefs } from 'pinia';
import ConfirmPopupModelComponent from './components/utils/ConfirmPopupModelComponent.vue';
export default {
    name: 'App',
    setup() {
        const appStore = useAppStore();
        const authStore = useAuthStore();
        const { popupFeedback } = storeToRefs(appStore)
        return {
            appStore,
            authStore,
            popupFeedback,
        }
    },
    components: {
        ConfirmPopupModelComponent,
    },
    data() {
        return {

        }
    },
    mounted() {
        initFlowbite();
    },
    methods: {
        displaySignoutPopup() {
            this.appStore.displayConfirmPopupModel("Are you sure to sign out your account?", this.signout)
        },
        signout() {
            this.authStore.signout();
            this.$router.go();
        }
    },
    watch: {
        popupFeedback: {
            handler(newValue, oldValue) {
                if (newValue === true) {
                    this.appStore.displayPageLoading(true)
                    setTimeout(() => {
                        this.appStore.displayPageLoading(false)
                        this.appStore.popupCallBack()
                    }, 1000)
                }
            },
        },
    }
};
</script>
