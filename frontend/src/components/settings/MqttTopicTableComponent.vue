<template>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg" v-if="allMqttTopic.length > 0">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        Topic name
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Description
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Config
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Status
                    </th>
                    <th scope="col" class="px-6 py-3">
                        Action
                    </th>
                </tr>
            </thead>
            <tbody>
                <tr class="bg-white border-b dark:bg-gray-800 dark:border-gray-700 border-gray-200"
                    v-for="data in allMqttTopic">
                    <th scope="row" class="px-6 py-4 font-medium text-gray-900 whitespace-nowrap dark:text-white">
                        {{ data.name }}
                    </th>
                    <td class="px-6 py-4">
                        {{ data.description }}
                    </td>
                    <td class="px-6 py-4">
                        {{ data.config }}
                    </td>
                    <td class="px-6 py-4 text-green-600" v-if="data.status == true">
                        Active
                    </td>
                    <td class="px-6 py-4 text-red-600" v-else>
                        Inactive
                    </td>
                    <td class="px-6 py-4">
                        <a href="#" class="font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        <p class="text-center italic py-3">There is no available MQTT Topic. Please create a new topic!</p>
    </div>
</template>

<script>
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
export default {
    props: {
        allMqttTopic:{
            type: Array,
            default: []
        }
    },
    setup() {
        const appStore = useAppStore();
        const settingStore = useSettingStore();
        return {
            appStore,
            settingStore
        }
    },
}
</script>