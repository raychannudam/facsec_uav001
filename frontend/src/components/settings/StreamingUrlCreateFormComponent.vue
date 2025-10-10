<template>
    <form class="rounded-md flex flex-row space-x-3 items-center" @submit.prevent="submitForm">
        <div class="relative">
            <input type="text" id="urlPrefix" v-model="urlPrefix"
                class="cursor-not-allowed block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required disabled />
            <label for="urlPrefix"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">URL Prefix *</label>
        </div>
        <div class="relative">
            <input type="text" id="urlName" v-model="urlName"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " required />
            <label for="urlName"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">URL
                Name *</label>
        </div>
        <div class="relative">
            <input type="text" id="urlDescription" v-model="urlDescription"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label for="urlDescription"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">URL
                Description</label>
        </div>
        <button type="submit"
            class="px-5 py-3 text-base font-medium text-center text-white bg-blue-700 rounded-lg hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Add
            new URL</button>
        <button type="button" @click="resetFormValues"
            class="px-5 py-3 text-base font-medium text-center text-white bg-red-700 rounded-lg hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">Cancel</button>
    </form>
</template>
<script>
import { initFlowbite } from 'flowbite';
import { handler } from 'flowbite/plugin';
export default {
    name: "MqttTopicCreateFormComponent",
    props: {
        streamingClientData: {
            type: Object
        }
    },
    data() {
        return {
            urlPrefix: `drsys/${this.streamingClientData.username}/`,
            urlName: "",
            urlDescription: ""
        };
    },
    mounted() {
        initFlowbite();
    },
    methods: {
        submitForm(){
            this.$emit("onSubmit", {
                streaming_client_id: this.streamingClientData.id,
                name: this.urlPrefix+this.urlName,
                description: this.urlDescription
            });
            this.resetFormValues();
        },
        resetFormValues(){
            this.urlName = ""
            this.urlDescription = ""
        },
    },
    watch:{
        
    }
}
</script>