<template>
    <div class="flex flex-col space-y-3">
        <div class="flex flex-col space-y-3">
            <div class="text-2xl font-bold flex items-center space-x-3">
                <span class="text-2xl material-symbols-outlined">
                    bigtop_updates
                </span>
                <p>Mqtt Client</p>
            </div>
            <p class="text-gray-600 dark:text-gray-400">Manage your data communication from sensors on drone with your
                application.</p>
            <MqttClientCreateFormComponent @onSubmit="onMqttClientCreateFormSubmit"
                id="mqtt_client_confirm_create_popup"></MqttClientCreateFormComponent>
            <hr class="border-0.5 border-gray-200">
            <MqttClientListComponent @onCompletedDeleteMqttClient="triggerCompletedDeleteMqttClient"
                @onMqttClientEditModalClose="mqttClientEditModalClosed" id="mqtt_client_list"
                :mqttClientList="allMqttClients" v-if="allMqttClients.length > 0"></MqttClientListComponent>
            <div v-else>
                <p class="text-center italic">There is no available MQTT Client. Please create a new client!</p>
            </div>
        </div>
        <div class="flex flex-col space-y-3">
            <div class="text-2xl font-bold flex items-center space-x-3">
                <span class="text-2xl material-symbols-outlined">
                    cast
                </span>
                <p>Streaming Client</p>
            </div>
            <p class="text-gray-600 dark:text-gray-400">Manage your streaming channels from the cameras on drone with
                your application.</p>
            <StreamingClientCreateFormComponent @onSubmit="onStreamingClientCreateFormSubmit"
                id="streaming_client_confirm_create_popup"></StreamingClientCreateFormComponent>
            <hr class="border-0.5 border-gray-200">
            <StreamingClientListComponent @onCompletedDeleteStreamingClient="triggerCompletedDeleteStreamingClient" :streamingClientList="allStreamingClients"  v-if="allStreamingClients.length > 0"></StreamingClientListComponent>
            <div v-else>
                <p class="text-center italic">There is no available Streaming Client. Please create a new client!</p>
            </div>
        </div>
    </div>
</template>
<script>
import MqttClientCreateFormComponent from '@/components/settings/MqttClientCreateFormComponent.vue';
import MqttClientListComponent from '@/components/settings/MqttClientListComponent.vue';
import StreamingClientCreateFormComponent from '@/components/settings/StreamingClientCreateFormComponent.vue';
import StreamingClientListComponent from '@/components/settings/StreamingClientListComponent.vue';
import { initFlowbite } from 'flowbite';
import { useSettingStore } from '@/stores/SettingStore';
import { useAppStore } from '@/stores/AppStore';

export default {
    name: "SettingsIndexView",
    setup() {
        const settingStore = useSettingStore();
        const appStore = useAppStore();
        return {
            settingStore,
            appStore,
        }
    },
    components: {
        MqttClientCreateFormComponent,
        MqttClientListComponent,
        StreamingClientCreateFormComponent,
        StreamingClientListComponent
    },
    data() {
        return {
            allMqttClients: [],
            allStreamingClients: []
        };
    },
    async mounted() {
        initFlowbite();
        await this.getAllMqttClients();
        await this.getAllStreamingClients();

    },
    methods: {
        async onMqttClientCreateFormSubmit(data) {
            this.appStore.displayPageLoading(true)
            let res = await this.settingStore.createMqttClient(data);
            this.appStore.displayPageLoading(false);
            this.appStore.displayRightToast(res.status, res.message);
            await this.getAllMqttClients();
        },
        async getAllMqttClients() {
            this.appStore.displayPageLoading(true)
            let res = await this.settingStore.getAllMqttClients();
            this.appStore.displayPageLoading(false)
            this.appStore.displayRightToast(res.status, res.message);
            if (res.status == "success") {
                this.allMqttClients = res.data
            }
        },
        async getAllStreamingClients() {
            this.appStore.displayPageLoading(true)
            let res = await this.settingStore.getAllStreamingClients();
            this.appStore.displayPageLoading(false)
            this.appStore.displayRightToast(res.status, res.message);
            if (res.status == "success") {
                this.allStreamingClients = res.data
            }
        },
        async triggerCompletedDeleteMqttClient() {
            await this.getAllMqttClients();
        },
        async mqttClientEditModalClosed() {
            await this.getAllMqttClients();
        },
        async onStreamingClientCreateFormSubmit(data){
            this.appStore.displayPageLoading(true)
            let res = await this.settingStore.createStreamingClient(data);
            this.appStore.displayPageLoading(false);
            this.appStore.displayRightToast(res.status, res.message);
            await this.getAllStreamingClients();
        },
        async triggerCompletedDeleteStreamingClient(){
            await this.getAllStreamingClients();
        }
    }
}
</script>