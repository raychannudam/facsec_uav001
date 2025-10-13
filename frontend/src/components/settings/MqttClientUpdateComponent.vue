<template>
    <PopupModalComponent :id="'popup-modal-detail' + data.id" @onSave="updateClient" @onClose="updateClientModalClosed">
        <template v-slot:header>
            <div>
                <p class="text-xs">Editing Mqtt client name <span class="block text-xl font-bold">{{ data.name }}</span>
                </p>
            </div>
        </template>
        <template v-slot:body>
            <div class="flex flex-col space-y-3">
                <fieldset class="text-xs relatvie flex flex-row space-x-3 items-center border dark:border-gray-600 rounded-md">
                    <legend class="text-gray-500 dark:text-gray-400 mx-3">Client Status</legend>
                    <div class="flex items-center ps-4 w-1/2 cursor-pointer">
                        <input id="active" type="radio" value="true" name="editingClientStatus" v-model="editingClientStatus"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 cursor-pointer">
                        <label for="active"
                            class="w-full py-4 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Active</label>
                    </div>
                    <div class="flex items-center ps-4 w-1/2 cursor-pointer">
                        <input id="inactive" type="radio" value="false" name="editingClientStatus" v-model="editingClientStatus"
                            class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600 cursor-pointer">
                        <label for="inactive"
                            class="w-full py-4 ms-2 text-sm font-medium text-gray-900 dark:text-gray-300 cursor-pointer">Inactive</label>
                    </div>
                </fieldset>
                <div class="relative">
                    <input type="text" id="editingClientName" v-model="editingClientName"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " />
                    <label for="editingClientName"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                        name </label>
                </div>
                <div class="relative">
                    <input type="text" id="editingClientDescription" v-model="editingClientDescription"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " />
                    <label for="editingClientDescription"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Client
                        name </label>
                </div>
            </div>
        </template>
    </PopupModalComponent>
</template>

<script>
import PopupModalComponent from '@/components/utils/PopupModalComponent.vue';
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
export default {
    props: {
        data: Object
    },
    components: {
        PopupModalComponent
    },
    setup(){
        const appStore = useAppStore();
        const settingStore = useSettingStore();
        return {
            appStore,
            settingStore,
        }
    },
    data() {
        return {
            editingClientName: this.data.name,
            editingClientDescription: this.data.description,
            editingClientStatus: this.data.status
        }
    },
    methods:{
        async updateClient(id){
            this.appStore.displayPageLoading(true)
            let data = {
                name: this.editingClientName,
                description: this.editingClientDescription,
                status: this.editingClientStatus,
                config: {}
            }
            let res = await this.settingStore.updateMqttClient(this.data.id, data);
            this.appStore.displayPageLoading(false)
            this.appStore.displayRightToast(res.status, res.message);

        },
        updateClientModalClosed(){
            this.$emit("onClose")
        }
    }
}
</script>