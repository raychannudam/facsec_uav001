<template>
    <div class="flex flex-row space-x-3 items-center justify-start relative">
        <p class="text-sm">{{ name }}</p>
        <button :id="id + 'Button'" :data-dropdown-toggle="id" data-dropdown-placement="bottom"
            class="text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center  flex-1  dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
            type="button">
            <p class="flex-1 start" v-if="!selectTopic">{{ dropDownDesc }}</p>
            <p class="flex-1 start" v-else>{{ selectTopic.name }}</p> <svg class="w-2.5 h-2.5 ms-3"
                aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
                <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                    d="m1 1 4 4 4-4" />
            </svg>
        </button>
        <!-- Dropdown menu -->
        <div :id="id" class="z-10 hidden bg-white rounded-lg shadow-sm w-full dark:bg-gray-700">
            <div class="p-3">
                <label :for="'search' + id" class="sr-only">Search</label>
                <div class="relative">
                    <div class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
                        <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                        </svg>
                    </div>
                    <input type="text" :id="'search' + id" v-model="query"
                        class="block w-full p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                        placeholder="Search topic...">
                </div>
            </div>
            <ul class="h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-700 dark:text-gray-200"
                :aria-labelledby="id + 'Button'">
                <li v-for="item in data">
                    <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
                        <input :id="'checkbox-item-' + id + '-' + item.name" type="radio" :value=item
                            v-model="selectTopic"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
                        <label :for="'checkbox-item-' + id + '-' + item.name"
                            class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">{{
                            item.name }}</label>
                    </div>
                </li>
            </ul>
        </div>
        <div class="relative" v-if="type != 'slider'">
            <input type="text" :id="id+'on'" v-model="onPayload"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-24 text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label :for="id+'on'"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">On
                Payload</label>
        </div>
        <div class="relative" v-else>
            <input type="text" :id="id+'min'" v-model="minPayload"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-24 text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label :for="id+'min'"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Min
                Payload</label>
        </div>
        <div class="relative" v-if="type != 'slider'">
            <input type="text" :id="id+'off'" v-model="offPayload"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-24 text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label :for="id+'off'"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Off
                Payload</label>
        </div>
        <div class="relative" v-else>
            <input type="text" :id="id+'max'" v-model="maxPayload"
                class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-24 text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                placeholder=" " />
            <label :for="id+'max'"
                class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Max
                Payload</label>
        </div>
    </div>
</template>
<script>
import { initFlowbite } from 'flowbite';
export default {
    props: ['id', 'name', 'dropDownDesc', 'type', 'data', 'selected'],
    data() {
        return {
            query: "",
            selectTopic: undefined,
            onPayload: "",
            offPayload: "",
            minPayload: "",
            maxPayload: "",
        }
    },
    methods: {
        topicSelected() {
            if (this.type != 'slider') {
                this.$emit("onTopicSelect", {
                    id: this.id,
                    name: this.name,
                    type: this.type,
                    selectedTopic: this.selectTopic,
                    onPayload: this.onPayload,
                    offPayload: this.offPayload,
                })
            } else {
                this.$emit("onTopicSelect", {
                    id: this.id,
                    name: this.name,
                    type: this.type,
                    selectedTopic: this.selectTopic,
                    minPayload: this.minPayload,
                    maxPayload: this.maxPayload,
                })
            }

        }
    },
    mounted(){
        initFlowbite();
        console.log(this.selected)
        if (Object.keys(this.selected).length != 0){
            this.selectTopic = this.selected
        }
    },
    watch: {
        selectTopic: {
            handler(newVal, oldVal) {
                if (newVal != oldVal) {
                    this.topicSelected();
                }
            }
        }
    }
}
</script>