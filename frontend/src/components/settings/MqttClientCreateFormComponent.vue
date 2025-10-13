<template>
    <form class="rounded-md flex flex-row space-x-3 items-center" @submit.prevent="submitForm">
        <div class="relative">
            <input type="text" id="mqttClientName" v-model="mqttClientName"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="mqttClientName"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                Name *</label>
        </div>
        <div class="relative">
            <input type="text" id="mqttClientDescription" v-model="mqttClientDescription"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label for="mqttClientDescription"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                Description</label>
        </div>
        <div class="relative">
            <input type="text" id="mqttClientUsername" v-model="mqttClientUsername" autocomplete="additional-name"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="mqttClientUsername"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                Username *</label>
        </div>
        <div class="relative">
            <input type="password" id="mqttClientPassword" v-model="mqttClientPassword" autocomplete="new-password"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="mqttClientPassword"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                Password *</label>
        </div>
        <button type="submit"
            class="px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add
            new client</button>
        <button type="reset"
            class="px-5 py-3 text-base font-medium text-center text-white bg-red-700 rounded-lg hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">Cancel</button>
    </form>
</template>
<script>
import { initFlowbite } from 'flowbite';
// import JsonEditorVue from 'json-editor-vue'
import 'vanilla-jsoneditor/themes/jse-theme-dark.css'

export default {
    name: "MqttClientCreateFormComponent",
    props: ["id"],
    components: {
        // JsonEditorVue
    },
    data() {
        return {
            mqttClientName: "",
            mqttClientUsername: "",
            mqttClientPassword: "",
            mqttClientDescription: "",
            mqttClientConfig: {}
        };
    },
    mounted() {
        initFlowbite();
    },
    methods: {
        submitForm() {
            this.$emit("onSubmit", {
                name: this.mqttClientName,
                username: this.mqttClientUsername,
                password: this.mqttClientPassword,
                description: this.mqttClientDescription
            });
            this.resetFormValues();
        },
        resetFormValues() {
            this.mqttClientName = ""
            this.mqttClientUsername = ""
            this.mqttClientPassword = ""
            this.mqttClientDescription = ""
        }
    }
}
</script>