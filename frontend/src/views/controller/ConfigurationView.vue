<template>
    <div class="flex flex-col space-y-3 h-full">
        <!-- Header -->
        <div class="flex flex-col w-full space-y-2">
            <!-- Title + Description -->
            <div class="flex flex-row items-center justify-between">
                <div>
                    <div class="flex flex-row items-center space-x-2">
                        <span class="text-2xl material-symbols-outlined">settings_input_component</span>
                        <p class="text-xl font-bold">Configuration</p>
                    </div>
                    <p class="text-xs text-gray-600 dark:text-gray-400 leading-tight">
                        Manage your control panel profiles.
                    </p>
                </div>
            </div>
        </div>

        <hr class="border-0.5 border-gray-200">

        <!-- SECTION 1: Profile Management -->
        <div class="flex flex-col space-y-3 p-4 bg-gray-50 dark:bg-gray-800 rounded-lg">
            <div class="flex flex-row items-center justify-between">
                <p class="text-sm font-bold">Profile Management</p>

                <!-- Profile Actions -->
                <div class="flex flex-wrap gap-2">
                    <!-- New Profile -->
                    <button @click="showCreateModal = true" class="flex items-center gap-1 px-3 py-1 text-xs font-medium text-white bg-green-700 hover:bg-green-800
                       rounded-lg focus:ring-2 focus:ring-green-300 dark:bg-green-600 dark:hover:bg-green-700">
                        <span class="material-symbols-outlined text-sm">add</span>
                        <span class="hidden sm:inline">New</span>
                    </button>

                    <!-- Delete Profile -->
                    <button v-if="selectedProfile" @click="showDeleteModal = true" class="flex items-center gap-1 px-3 py-1 text-xs font-medium text-white bg-red-700 hover:bg-red-800
                       rounded-lg focus:ring-2 focus:ring-red-300">
                        <span class="material-symbols-outlined text-sm">delete</span>
                        <span class="hidden sm:inline">Delete</span>
                    </button>
                </div>
            </div>

            <!-- Profile Selection -->
            <div class="flex flex-row space-x-3 items-center justify-start">
                <p class="text-sm font-medium">Selected Profile:</p>
                <button id="selectProfileDropdownButton" data-dropdown-toggle="selectProfileDropdown"
                    data-dropdown-placement="bottom"
                    class="focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
                    type="button">
                    <p v-if="!selectedProfile">Select a Profile</p>
                    <p v-else>{{ selectedProfile.name }}</p>
                    <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                        viewBox="0 0 10 6">
                        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                            d="m1 1 4 4 4-4" />
                    </svg>
                </button>
                <!-- Profile Dropdown -->
                <div id="selectProfileDropdown" class="z-10 hidden bg-white rounded-lg shadow-sm w-60 dark:bg-gray-700">
                    <div class="p-3">
                        <label for="profileSearchQuery" class="sr-only">Search</label>
                        <div class="relative">
                            <div
                                class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
                                <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                                    xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                                    <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round"
                                        stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                                </svg>
                            </div>
                            <input type="text" id="profileSearchQuery" v-model="profileSearchQuery"
                                class="block w-full p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                                placeholder="Search profile...">
                        </div>
                    </div>
                    <ul class="h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-700 dark:text-gray-200"
                        aria-labelledby="selectProfileDropdownButton">
                        <li v-for="profile in filteredProfiles" :key="profile.id">
                            <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input :id="'profile-' + profile.id" type="radio" :value="profile"
                                    v-model="selectedProfile" @change="onProfileSelect"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                                <label :for="'profile-' + profile.id"
                                    class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">
                                    {{ profile.name }}
                                </label>
                            </div>
                        </li>
                        <li v-if="filteredProfiles.length === 0">
                            <p class="py-2 text-center text-gray-500">No profiles found</p>
                        </li>
                    </ul>
                </div>
            </div>
        </div>

        <hr class="border-0.5 border-gray-200">

        <!-- SECTION 2: Configuration Settings -->
        <div v-if="selectedProfile" class="flex flex-col space-y-3">
            <!-- Configuration Header with Actions -->
            <div class="flex flex-row items-center justify-between">
                <p class="text-sm font-bold">Configuration Settings</p>

                <!-- Configuration Actions -->
                <div class="flex flex-wrap gap-2">
                    <!-- Edit -->
                    <button v-if="!isEditing" @click="isEditing = true" class="flex items-center gap-1 px-3 py-1 text-xs font-medium text-white bg-yellow-600 hover:bg-yellow-700
                       rounded-lg focus:ring-2 focus:ring-yellow-300">
                        <span class="material-symbols-outlined text-sm">edit_note</span>
                        <span class="hidden sm:inline">Edit</span>
                    </button>

                    <!-- Cancel -->
                    <button v-if="isEditing" @click="cancel" class="flex items-center gap-1 px-3 py-1 text-xs font-medium text-white bg-red-700 hover:bg-red-800
                       rounded-lg focus:ring-2 focus:ring-red-300">
                        <span class="material-symbols-outlined text-sm">cancel</span>
                        <span class="hidden sm:inline">Cancel</span>
                    </button>

                    <!-- Save -->
                    <button v-if="isEditing" @click="saveProfile" class="flex items-center gap-1 px-3 py-1 text-xs font-medium text-white bg-blue-700 hover:bg-blue-800
                       rounded-lg focus:ring-2 focus:ring-blue-300">
                        <span class="material-symbols-outlined text-sm">save</span>
                        <span class="hidden sm:inline">Save</span>
                    </button>
                </div>
            </div>

            <div class="flex flex-col space-y-3 h-[50vh] overflow-scroll relative">
                <!-- Select UAV -->
                <div class="flex flex-row space-x-3 items-center justify-start"
                    :class="{ 'pointer-events-none opacity-70': !isEditing }">
                    <p class="text-sm font-bold">Selected UAV</p>
                    <button id="selectDroneDropdownSearchButton" data-dropdown-toggle="selectDroneDropdownSearch"
                        data-dropdown-placement="bottom"
                        class="focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
                        type="button">
                        <p v-if="!selectedDrone">Select a UAV</p>
                        <p v-else>{{ selectedDrone.name }}</p>
                        <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none"
                            viewBox="0 0 10 6">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m1 1 4 4 4-4" />
                        </svg>
                    </button>
                </div>

                <!-- Drone Dropdown -->
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
                        <li v-for="drone in allDrones" :key="drone.id">
                            <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                                <input :id="drone.id" type="radio" :value="drone" v-model="selectedDrone"
                                    @change="selectDrone"
                                    class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                                <label :for="drone.id"
                                    class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">
                                    {{ drone.name }}
                                </label>
                            </div>
                        </li>
                    </ul>
                </div>

                <!-- Rest of the content with proper disabled state -->
                <div :class="{ 'pointer-events-none opacity-70': !isEditing }">
                    <div class="flex items-center justify-center">
                        <img src="https://www.uavfordrone.com/wp-content/uploads/2019/05/%E7%BB%8F%E7%BA%AC-M600-Pro-%E9%9B%86%E5%A4%A7%E6%88%90%EF%BC%8C%E8%BE%BE%E8%BF%9C%E8%A7%81-DJI-%E5%A4%A7%E7%96%86%E5%88%9B%E6%96%B0-3.png"
                            class="h-40" alt="">
                    </div>

                    <!-- Streaming URL Section -->
                    <div class="pb-2 border-dashed border-b">
                        <p class="font-bold">Streaming URLs</p>
                    </div>
                    <div class="flex flex-col space-y-3" v-if="availableStreamingUrls.length > 0">
                        <StreamingUrlAssignComponent v-for="streamingUrl in config.streamingUrls" :key="streamingUrl.id"
                            type="streaming" :id="streamingUrl.id" :name="streamingUrl.name"
                            :selected="streamingUrl.selectedUrl" dropDownDesc="Select a streaming URL"
                            :data="availableStreamingUrls" @onUrlSelect="assignStreamingUrl" />
                    </div>

                    <!-- Data Communication -->
                    <div class="pb-2 border-dashed border-b">
                        <p class="font-bold">Data Communication</p>
                    </div>
                    <div class="flex flex-col space-y-3" v-if="availableMqttTopics.length > 0">
                        <TopicAssignComponent v-for="mqttTopic in config.mqttTopics" :key="mqttTopic.id"
                            :type="mqttTopic.type" :id="mqttTopic.id" :name="mqttTopic.name"
                            dropDownDesc="Select a topic" :data="availableMqttTopics" @onTopicSelect="assignTopic"
                            :selected="{
                                'selectedTopic': mqttTopic.selectedTopic,
                                'onPayload': mqttTopic.onPayload,
                                'offPayload': mqttTopic.offPayload,
                                'minPayload': mqttTopic.minPayload,
                                'maxPayload': mqttTopic.maxPayload
                            }" />
                    </div>
                </div>
            </div>
        </div>

        <div v-else class="flex items-center justify-center h-[50vh]">
            <p class="text-gray-500 dark:text-gray-400">Please select or create a profile to get started</p>
        </div>
    </div>

    <!-- Modals -->
    <CreateProfileModal :isOpen="showCreateModal" @close="showCreateModal = false" @create="handleCreateProfile" />

    <DeleteModal :isOpen="showDeleteModal" :title="'Confirm Profile Deletion'"
        :message="`Are you sure you want to delete this profile? This will permanently remove all profile configurations and settings.`"
        :confirmText="'Delete'" :itemId="selectedProfile?.id" @close="showDeleteModal = false"
        @confirm="handleDeleteProfile" />
</template>

<script>
import { initFlowbite } from 'flowbite';
import { useUavStore } from '@/stores/UavStore';
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
import { useControllerStore } from '@/stores/ControllerStore';
import TopicAssignComponent from '@/components/controller/TopicAssignComponent.vue';
import StreamingUrlAssignComponent from '@/components/controller/StreamingUrlAssignComponent.vue';
import CreateProfileModal from '@/components/controller/CreateProfileModal.vue';
import DeleteModal from '@/components/utils/DeleteModal.vue';

export default {
    components: {
        TopicAssignComponent,
        StreamingUrlAssignComponent,
        CreateProfileModal,
        DeleteModal
    },
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
            allProfiles: [],
            selectedProfile: null,
            profileSearchQuery: "",
            allDrones: [],
            droneSearchQuery: "",
            selectedDrone: undefined,
            availableMqttTopics: [],
            availableStreamingUrls: [],
            isEditing: false,
            config: this.getDefaultConfig(),
            showCreateModal: false,
            showDeleteModal: false
        }
    },
    computed: {
        filteredProfiles() {
            if (!this.profileSearchQuery) return this.allProfiles;
            return this.allProfiles.filter(profile =>
                profile.name.toLowerCase().includes(this.profileSearchQuery.toLowerCase())
            );
        }
    },
    async mounted() {
        initFlowbite();
        await this.loadProfiles();
        await this.getAllDrone();
    },
    methods: {
        getDefaultConfig() {
            return {
                name: '',
                description: '',
                selectedDrone: {},
                streamingUrls: [
                    { id: 'stream1', name: 'CAM 01 Streaming URL', selectedUrl: {} },
                    { id: 'stream2', name: 'CAM 02 Streaming URL', selectedUrl: {} },
                    { id: 'stream3', name: 'CAM 03 Streaming URL', selectedUrl: {} },
                    { id: 'stream4', name: 'CAM 04 Streaming URL', selectedUrl: {} },
                ],
                mqttTopics: [
                    { id: 'btn1', type: 'button', name: "Button 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn2', type: 'button', name: "Button 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn3', type: 'button', name: "Button 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn4', type: 'button', name: "Button 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn5', type: 'button', name: "Button 05", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn6', type: 'button', name: "Button 06", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'btn7', type: 'button', name: "Button 07", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt1', type: 'switch', name: "Switch 01", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt2', type: 'switch', name: "Switch 02", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt3', type: 'switch', name: "Switch 03", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt4', type: 'switch', name: "Switch 04", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt5', type: 'switch', name: "Switch 05", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt6', type: 'switch', name: "Switch 06", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'swt7', type: 'switch', name: "Switch 07", onPayload: "1", offPayload: "0", selectedTopic: {} },
                    { id: 'sld1', type: 'slider', name: "Slider 01", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld2', type: 'slider', name: "Slider 02", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld3', type: 'slider', name: "Slider 03", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld4', type: 'slider', name: "Slider 04", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld5', type: 'slider', name: "Slider 05", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld6', type: 'slider', name: "Slider 06", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                    { id: 'sld7', type: 'slider', name: "Slider 07", maxPayload: "1000", minPayload: "100", selectedTopic: {} },
                ]
            };
        },

        async loadProfiles() {
            let res = await this.controllerStore.getAllControllers();
            if (res.status === "success") {
                this.allProfiles = res.data;
                if (this.allProfiles.length > 0) {
                    this.selectedProfile = this.allProfiles[0];
                    this.controllerStore.selectController(this.selectedProfile);
                    this.loadProfileConfig();
                }
            }
        },

        async onProfileSelect() {
            this.isEditing = false;
            this.availableMqttTopics = [];
            this.availableStreamingUrls = [];

            // Update the store's selected controller
            this.controllerStore.selectController(this.selectedProfile);

            this.loadProfileConfig();

            await this.$nextTick();
            initFlowbite();
        },

        loadProfileConfig() {
            if (!this.selectedProfile) return;

            const defaultConfig = this.getDefaultConfig();

            let mqttTopics = [];
            if (this.selectedProfile.config?.mqttTopics && this.selectedProfile.config.mqttTopics.length > 0) {
                mqttTopics = defaultConfig.mqttTopics.map(defaultTopic => {
                    const savedTopic = this.selectedProfile.config.mqttTopics.find(t => t.id === defaultTopic.id);
                    if (savedTopic) {
                        return {
                            ...defaultTopic,
                            ...savedTopic,
                            selectedTopic: savedTopic.selectedTopic || {}
                        };
                    }
                    return defaultTopic;
                });
            } else {
                mqttTopics = defaultConfig.mqttTopics;
            }

            this.config = {
                name: this.selectedProfile.name,
                description: this.selectedProfile.description,
                selectedDrone: this.selectedProfile.config?.selectedDrone || {},
                streamingUrls: this.selectedProfile.config?.streamingUrls || defaultConfig.streamingUrls,
                mqttTopics: mqttTopics
            };

            console.log('📝 Loaded config for profile:', this.selectedProfile.name);
            console.log('📋 MQTT Topics loaded:', this.config.mqttTopics.filter(t => t.selectedTopic?.name).length);

            const hasDrone = this.config.selectedDrone &&
                typeof this.config.selectedDrone === 'object' &&
                Object.keys(this.config.selectedDrone).length > 0 &&
                this.config.selectedDrone.id &&
                this.config.selectedDrone.mqtt_client_id &&
                this.config.selectedDrone.streaming_client_id;

            if (hasDrone) {
                this.selectedDrone = this.config.selectedDrone;
                console.log('🚁 Loading resources for drone:', this.selectedDrone.name);
                this.loadDroneResources();
            } else {
                console.log('⚠️ No drone configured for this profile');
                this.selectedDrone = undefined;
                this.availableMqttTopics = [];
                this.availableStreamingUrls = [];
            }
        },

        async selectDrone() {
            if (!this.selectedDrone) return;

            console.log('🚁 Drone selected:', this.selectedDrone.name);

            // Load the new drone's available resources
            await this.loadDroneResources();

            // Update the config with the new drone
            this.config.selectedDrone = this.selectedDrone;

            // Keep existing topic/URL configurations - don't reset!
            console.log('✅ Drone updated, existing configurations preserved');
        },

        async loadDroneResources() {
            if (!this.selectedDrone ||
                typeof this.selectedDrone !== 'object' ||
                !this.selectedDrone.mqtt_client_id ||
                !this.selectedDrone.streaming_client_id) {
                console.log('⚠️ No drone selected or missing required client IDs');
                this.availableMqttTopics = [];
                this.availableStreamingUrls = [];
                return;
            }

            console.log('🔍 Loading topics for mqtt_client_id:', this.selectedDrone.mqtt_client_id);

            try {
                let mqttTopicRes = await this.settingStore.getAllMqttTopicByMqttClientId(this.selectedDrone.mqtt_client_id);
                let streamingUrlRes = await this.settingStore.getAllStreamingUrls(this.selectedDrone.streaming_client_id);

                if (mqttTopicRes.status === "success") {
                    this.availableMqttTopics = mqttTopicRes.data.filter(topic => !topic.is_default);
                    console.log('✅ Available MQTT topics loaded:', this.availableMqttTopics.length);
                }
                if (streamingUrlRes.status === "success") {
                    this.availableStreamingUrls = streamingUrlRes.data;
                    console.log('✅ Available streaming URLs loaded:', this.availableStreamingUrls.length);
                }
            } catch (error) {
                console.error('❌ Error loading drone resources:', error);
                this.availableMqttTopics = [];
                this.availableStreamingUrls = [];
            }
        },

        assignTopic(data) {
            const mqttTopic = this.config.mqttTopics.find(item => item.id === data.id);
            if (mqttTopic) {
                mqttTopic.name = data.name;
                mqttTopic.selectedTopic = data.selectedTopic;
                mqttTopic.minPayload = data.minPayload;
                mqttTopic.maxPayload = data.maxPayload;
                mqttTopic.onPayload = data.onPayload;
                mqttTopic.offPayload = data.offPayload;
                console.log('✅ Topic assigned:', data.name, 'to', data.id);
            }
        },

        assignStreamingUrl(data) {
            const streamingUrl = this.config.streamingUrls.find(item => item.id === data.id);
            if (streamingUrl) {
                streamingUrl.selectedUrl = data.selectedUrl;
                console.log('✅ Streaming URL assigned to', data.id);
            }
        },

        resetUrlsAndTopics() {
            if (!confirm('Are you sure you want to reset all topic and URL configurations? This cannot be undone.')) {
                return;
            }

            console.log('🔄 Resetting all topics and URLs to defaults');
            this.config.streamingUrls = this.getDefaultConfig().streamingUrls;
            this.config.mqttTopics = this.getDefaultConfig().mqttTopics;
        },

        async saveProfile() {
            if (!this.selectedProfile) return;

            const currentProfileId = this.selectedProfile.id;

            const data = {
                name: this.selectedProfile.name,
                description: this.config.description || this.selectedProfile.description,
                config: {
                    selectedDrone: this.config.selectedDrone,
                    streamingUrls: this.config.streamingUrls,
                    mqttTopics: this.config.mqttTopics,
                    default: this.selectedProfile.config?.default || {}
                }
            };

            console.log('💾 Saving profile with topics:', data.config.mqttTopics.filter(t => t.selectedTopic?.name).length);

            this.appStore.displayPageLoading(true);
            let res = await this.controllerStore.updateController(currentProfileId, data);
            this.appStore.displayPageLoading(false);

            if (res.status === "success") {
                this.isEditing = false;
                await this.loadProfiles();
                this.selectedProfile = this.allProfiles.find(p => p.id === currentProfileId);
                if (this.selectedProfile) {
                    this.controllerStore.selectController(this.selectedProfile);
                    this.loadProfileConfig();
                }
                await this.$nextTick();
                initFlowbite();
                this.$emit("onUpdate");
                console.log('✅ Profile saved successfully');
            }
        },

        async cancel() {
            this.isEditing = false;
            this.loadProfileConfig();
            await this.$nextTick();
            initFlowbite();
        },

        async getAllDrone(query = "") {
            let res = await this.uavStore.getAllUavs(query);
            if (res.status === "success") {
                this.allDrones = res.data;
            }
        },


        async handleCreateProfile(profileData) {
            this.appStore.displayPageLoading(true);

            const newProfileData = {
                name: profileData.name,
                description: profileData.description,
                config: {
                    selectedDrone: {},
                    streamingUrls: this.getDefaultConfig().streamingUrls,
                    mqttTopics: this.getDefaultConfig().mqttTopics,
                    default: {
                        mqttTopics: []
                    }
                }
            };

            let res = await this.controllerStore.createController(newProfileData);
            this.appStore.displayPageLoading(false);

            if (res.status === "success") {
                this.showCreateModal = false;
                await this.loadProfiles();
                this.selectedProfile = this.allProfiles.find(p => p.name === profileData.name);
                if (this.selectedProfile) {
                    this.loadProfileConfig();
                }
                this.isEditing = true;
                this.$emit("onUpdate");
                // Reinitialize Flowbite after profile creation
                await this.$nextTick();
                initFlowbite();
            }
        },


        async handleDeleteProfile() {
            if (!this.selectedProfile) return;

            this.appStore.displayPageLoading(true);
            let res = await this.controllerStore.deleteController(this.selectedProfile.id);
            this.appStore.displayPageLoading(false);

            if (res.status === "success") {
                this.showDeleteModal = false;
                await this.loadProfiles();
                this.selectedProfile = this.allProfiles.length > 0 ? this.allProfiles[0] : null;
                if (this.selectedProfile) {
                    this.loadProfileConfig();
                }
                this.$emit("onUpdate");
                // Reinitialize Flowbite after profile deletion
                await this.$nextTick();
                initFlowbite();
            }
        },
    },

    watch: {
        droneSearchQuery: {
            async handler(newVal, oldVal) {
                if (newVal !== oldVal) {
                    await this.getAllDrone(newVal);
                }
            }
        },
        // Reinitialize Flowbite when editing state changes
        isEditing: {
            async handler() {
                await this.$nextTick();
                initFlowbite();
            }
        },
        selectedProfile: {
            handler(newProfile) {
                if (newProfile) {
                    console.log('🔄 Profile changed in ConfigurationView:', newProfile.name);
                    this.controllerStore.selectController(newProfile);
                }
            },
            deep: true
        },
    }
}
</script>