<template>
    <form class="rounded-md flex flex-row space-x-3 items-center" @submit.prevent="submitForm">
        <div class="relative">
            <input type="text" id="mqttTopicPrefix" v-model="mqttTopicPrefix"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required readonly />
            <label for="mqttTopicPrefix"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Topic Prefix *</label>
        </div>
        <div class="relative">
            <input type="text" id="mqttTopicName" v-model="mqttTopicName"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="mqttTopicName"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Topic
                Name *</label>
        </div>
        <div class="relative">
            <input type="text" id="mqttTopicDescription" v-model="mqttTopicDescription"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label for="mqttTopicDescription"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Topic
                Description</label>
        </div>
        <button type="submit"
            class="px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add
            new topic</button>
        <button type="reset"
            class="px-5 py-3 text-base font-medium text-center text-white bg-red-700 rounded-lg hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">Cancel</button>
    </form>
</template>
<script>
import { initFlowbite } from 'flowbite';
export default {
    name: "MqttTopicCreateFormComponent",
    props: {
        mqttClientData: {
            type: Object
        }
    },
    data() {
        return {
            mqttTopicPrefix: `drsys/${this.mqttClientData.username}/`,
            mqttTopicName: "",
            mqttTopicDescription: ""
        };
    },
    mounted() {
        initFlowbite();
    },
    methods: {
        submitForm(){
            this.$emit("onSubmit", {
                mqtt_client_id: this.mqttClientData.id,
                name: this.mqttTopicPrefix+this.mqttTopicName,
                description: this.mqttTopicDescription
            });
            this.resetFormValues();
        },
        resetFormValues(){
            this.mqttTopicName = ""
            this.mqttTopicDescription = ""
        }
    }
}
</script>