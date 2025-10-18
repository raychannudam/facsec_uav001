<template>
    <div class="flex flex-col space-y-3 h-full">
        <div class="flex flex-row space-x-3 items-end justify-between">
            <div class="flex flex-col items-start space-y-3">
                <div class="text-2xl  font-bold flex flex-row space-x-3">
                    <span class="text-2xl material-symbols-outlined">
                        settings_input_component
                    </span>
                    <p>Configuration</p>
                </div>
                <p class="text-gray-600 dark:text-gray-400">Manage your control panel.</p>
            </div>
            <div class="flex flex-row space-x-3">
                <button type="button" @click="isEditing = true" v-if="!isEditing"
                    class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:outline-none focus:ring-yellow-300 rounded-lg text-center dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800">
                    <span class="material-symbols-outlined">
                        edit_note
                    </span>
                    <p>Edit</p>
                </button>
                <button type="button" @click="cancle" v-if="isEditing"
                    class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-yellow-800">
                    <span class="material-symbols-outlined">
                        cancel
                    </span>
                    <p>Cancel</p>
                </button>
                <button type="button" @click="updateController"
                    class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
                    <span class="material-symbols-outlined">
                        save
                    </span>
                    <p>Save</p>
                </button>
            </div>
        </div>

        <hr class="border-0.5 border-gray-200">
        <div class="flex flex-col space-y-3 h-[50vh] overflow-scroll relative"
            :class="{ 'pointer-events-none  opacity-50': !isEditing }">
            <!-- Select UAV -->
            <div class="flex flex-row space-x-3 items-center justify-start">
                <p class="text-sm font-bold">Selected UAV</p>
                <button id="selectDroneDropdownSearchButton" data-dropdown-toggle="selectDroneDropdownSearch"
                    data-dropdown-placement="bottom"
                    class="text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center   dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
                    type="button">
                    <p v-if="!selectedDrone">Select a UAV</p>
                    <p v-else>{{ selectedDrone.name }}</p> <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true"
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
                        <li v-for="drone in allDrones" v-if="allDrones.length > 0">
                            <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input :id="drone.id" type="radio" :value=drone v-model="selectedDrone"
                                    @change="selectDrone"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                                <label :for="drone.id"
                                    class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">{{
                                        drone.name }}</label>
                            </div>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="flex items-center justify-center">
                <img src="https://www.uavfordrone.com/wp-content/uploads/2019/05/%E7%BB%8F%E7%BA%AC-M600-Pro-%E9%9B%86%E5%A4%A7%E6%88%90%EF%BC%8C%E8%BE%BE%E8%BF%9C%E8%A7%81-DJI-%E5%A4%A7%E7%96%86%E5%88%9B%E6%96%B0-3.png"
                    class="h-40" alt="">
            </div>
            <!-- Streaming URL Section -->
            <div class="pb-2 border-dashed border-b">
                <p class="font-bold">Streaming URLs</p>
            </div>
            <div class="flex flex-col space-y-3" v-if="availableStreamingUrls.length > 0">
                <StreamingUrlAssignComponent v-for="streamingUrl in config.streamingUrls" type="streaming"
                    :id="streamingUrl.id" :name="streamingUrl.name" :selected="streamingUrl.selectedUrl"
                    dropDownDesc="Select a streaming URL" :data="availableStreamingUrls" :key="streamingUrl.selectedUrl"
                    @onUrlSelect="assignStreamingUrl" />
            </div>
            <!-- Data Communication -->
            <div class="pb-2 border-dashed border-b">
                <p class="font-bold">Data Communication</p>
            </div>
            <div class="flex flex-col space-y-3" v-if="availableMqttTopics.length > 0">
                <TopicAssignComponent v-for="mqttTopic in config.mqttTopics" :type="mqttTopic.type" :id="mqttTopic.id"
                    :name="mqttTopic.name" dropDownDesc="Select a topic" :data="availableMqttTopics"
                    @onTopicSelect="assignTopic" :selected="{
                        'selectedTopic': mqttTopic.selectedTopic,
                        'onPayload': mqttTopic.onPayload,
                        'offPayload': mqttTopic.offPayload,
                        'minPayload': mqttTopic.minPayload,
                        'maxPayload': mqttTopic.maxPayload
                    }"
                    :key="mqttTopic.selectedTopic"></TopicAssignComponent>
            </div>

        </div>
    </div>
</template>
<script>
import { initFlowbite } from 'flowbite';
import { useUavStore } from '@/stores/UavStore';
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
import { useControllerStore } from '@/stores/Controller';
import TopicAssignComponent from '@/components/controller/TopicAssignComponent.vue';
import StreamingUrlAssignComponent from '@/components/controller/StreamingUrlAssignComponent.vue';
export default {
    components: { TopicAssignComponent, StreamingUrlAssignComponent },
    setup() {
        const uavStore = useUavStore();
        const appStore = useAppStore();
        const settingStore = useSettingStore();
        const controllerStore = useControllerStore();
        return {
            uavStore,
            appStore,
            settingStore,
            controllerStore
        }
    },
    data() {
        return {
            allDrones: [],
            droneSearchQuery: "",
            selectedDrone: undefined,
            availableMqttTopics: [],
            availableStreamingUrls: [],
            isEditing: false,
            myController: undefined,
            config: {
                'selectedDrone': {},
                'streamingUrls': [
                    { id: 'stream1', name: 'CAM 01 Streaming URL', selectedUrl: {} },
                    { id: 'stream2', name: 'CAM 02 Streaming URL', selectedUrl: {} },
                    { id: 'stream3', name: 'CAM 03 Streaming URL', selectedUrl: {} },
                    { id: 'stream4', name: 'CAM 04 Streaming URL', selectedUrl: {} },
                ],
                'mqttTopics': [
                    { id: 'btn1', type: 'button', name: "Button 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn2', type: 'button', name: "Button 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn3', type: 'button', name: "Button 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn4', type: 'button', name: "Button 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt1', type: 'switch', name: "Switch 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt2', type: 'switch', name: "Switch 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt3', type: 'switch', name: "Switch 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt4', type: 'switch', name: "Switch 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'sld1', type: 'slider', name: "Slider 01", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                    { id: 'sld2', type: 'slider', name: "Slider 02", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                    { id: 'sld3', type: 'slider', name: "Slider 03", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                    { id: 'sld4', type: 'slider', name: "Slider 04", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                ],
            }
        }
    },
    async mounted() {
        initFlowbite();
        await this.getAllController();
        await this.getAllDrone();
    },
    methods: {
        async getAllDrone(query = "") {
            let res = await this.uavStore.getAllUavs(query);
            if (res.status == "success") {
                this.allDrones = res.data
            }
        },
        assignTopic(data) {
            console.log(data)
            const mqttTopic = this.config.mqttTopics.find(item => item.id == data.id)
            if (mqttTopic) {
                mqttTopic.selectedTopic = data.selectedTopic
                mqttTopic.minPayload = data.minPayload
                mqttTopic.maxPayload = data.maxPayload
                mqttTopic.onPayload = data.onPayload
                mqttTopic.offPayload = data.offPayload
            }
        },
        assignStreamingUrl(data) {
            // console.log(data)
            const streamingUrl = this.config.streamingUrls.find(item => item.id == data.id)
            if (streamingUrl) {
                streamingUrl.selectedUrl = data.selectedUrl
            }
        },
        async getAllController() {
            this.appStore.displayPageLoading(true);
            let res = await this.controllerStore.getAllControllers();
            this.appStore.displayPageLoading(false)
            if (res.status == "success") {
                this.myController = res.data[0]
                if (
                    Object.keys(this.myController.config['selectedDrone']).length != 0
                ) {
                    this.selectedDrone = this.myController.config['selectedDrone']
                }
                if (this.myController.config['streamingUrls'].length > 0) {
                    this.config.streamingUrls = this.myController.config['streamingUrls']
                }
                if (this.myController.config['mqttTopics'].length > 0) {
                    this.config.mqttTopics = this.myController.config['mqttTopics']
                }
            }

        },
        async updateController() {
            if (this.isEditing == true) {
                let data = {
                    'name': this.myController.name,
                    'description': this.myController.description,
                    "config": this.config
                }
                this.appStore.displayPageLoading(true);
                let res = await this.controllerStore.updateController(this.myController.id, data);
                this.appStore.displayPageLoading(false);
                this.appStore.displayRightToast(res.status, res.message);
                await this.getAllController();
            }
            this.isEditing = false;
            await this.getAllController();
            this.$emit("onUpdate")
        },
        async selectDrone() {
            let mqttTopicRes = await this.settingStore.getAllMqttTopicByMqttClientId(this.selectedDrone.mqtt_client_id)
            let streamingUrlRes = await this.settingStore.getAllStreamingUrls(this.selectedDrone.streaming_client_id)
            if (mqttTopicRes.status == "success") {
                this.availableMqttTopics = mqttTopicRes.data
            }
            if (streamingUrlRes.status == "success") {
                this.availableStreamingUrls = streamingUrlRes.data
            }
            this.config.selectedDrone = this.selectedDrone;
            this.resetUrlsAndTopics();
        },
        resetUrlsAndTopics() {
            this.config.streamingUrls = [
                { id: 'stream1', name: 'CAM 01 Streaming URL', selectedUrl: {} },
                { id: 'stream2', name: 'CAM 02 Streaming URL', selectedUrl: {} },
                { id: 'stream3', name: 'CAM 03 Streaming URL', selectedUrl: {} },
                { id: 'stream4', name: 'CAM 04 Streaming URL', selectedUrl: {} },
            ];
            this.config.mqttTopics = [
                { id: 'btn1', type: 'button', name: "Button 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'btn2', type: 'button', name: "Button 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'btn3', type: 'button', name: "Button 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'btn4', type: 'button', name: "Button 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'swt1', type: 'switch', name: "Switch 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'swt2', type: 'switch', name: "Switch 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'swt3', type: 'switch', name: "Switch 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'swt4', type: 'switch', name: "Switch 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                { id: 'sld1', type: 'slider', name: "Slider 01", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                { id: 'sld2', type: 'slider', name: "Slider 02", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                { id: 'sld3', type: 'slider', name: "Slider 03", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
                { id: 'sld4', type: 'slider', name: "Slider 04", maxPayload: "100", minPayload: "1000", selectedTopic: {} },
            ];
        },
        async cancle() {
            this.isEditing = false;
            await this.getAllController();
        }
    },
    watch: {
        droneSearchQuery: {
            async handler(newVal, oldVal) {
                if (newVal != oldVal) {
                    await this.getAllDrone(newVal);
                }
            }
        },
        selectedDrone: {
            async handler(newVal, oldVal) {
                if (newVal != oldVal) {
                    let mqttTopicRes = await this.settingStore.getAllMqttTopicByMqttClientId(newVal.mqtt_client_id)
                    let streamingUrlRes = await this.settingStore.getAllStreamingUrls(newVal.streaming_client_id)
                    if (mqttTopicRes.status == "success") {
                        this.availableMqttTopics = mqttTopicRes.data
                    }
                    if (streamingUrlRes.status == "success") {
                        this.availableStreamingUrls = streamingUrlRes.data
                    }
                    this.config.selectedDrone = newVal
                }
            }
        }
    }

}
</script>