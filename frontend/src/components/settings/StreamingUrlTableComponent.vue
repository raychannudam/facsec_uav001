<template>
    <div class="relative overflow-x-auto shadow-md sm:rounded-lg" v-if="allStreamingUrls.length > 0">
        <table class="w-full text-sm text-left rtl:text-right text-gray-500 dark:text-gray-400">
            <thead class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-700 dark:text-gray-400">
                <tr>
                    <th scope="col" class="px-6 py-3">
                        Streaming name/path
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
                    v-for="data in allStreamingUrls">
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
                    <td class="px-6 py-4 flex items-center space-x-3">
                        <!-- <a type="button"
                            class="cursor-pointer font-medium text-blue-600 dark:text-blue-500 hover:underline">Edit</a> -->
                        <a type="button" @click="displayStreamingUrlDeleteComfirmPopup(data.id)"
                            :data-modal-target="'delete_streaming_url_confirm_popup' + data.id"
                            :data-modal-toggle="'delete_streaming_url_confirm_popup' + data.id"
                            class="cursor-pointer font-medium text-red-600 dark:text-red-500 hover:underline">Delete</a>
                        <ConfirmPopupModelComponent :model_id="'delete_streaming_url_confirm_popup' + data.id">
                        </ConfirmPopupModelComponent>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    <div v-else>
        <p class="text-center italic py-3">There is no available Streaming URL. Please create a new URL!</p>
    </div>
</template>

<script>
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
import ConfirmPopupModelComponent from '../utils/ConfirmPopupModelComponent.vue';
import { storeToRefs } from 'pinia';
export default {
    props: {
        allStreamingUrls: {
            type: Array,
            default: []
        }
    },
    setup() {
        const appStore = useAppStore();
        const settingStore = useSettingStore();
        const { popupFeedback } = storeToRefs(appStore);
        return {
            appStore,
            settingStore,
            popupFeedback
        }
    },
    components: {
        ConfirmPopupModelComponent
    },
    data(){
        return {
            toDeleteStreamingUrlId: undefined
        }
    },
    methods:{
        displayStreamingUrlDeleteComfirmPopup(id){
            this.toDeleteStreamingUrlId = id
            this.appStore.displayConfirmPopupModel("Are you sure to delete this topic?", this.deleteStreamingUrl)
        },
        async deleteStreamingUrl(){
            this.appStore.displayPageLoading(true)
            let res = await this.settingStore.deleteStreamingUrl(this.toDeleteStreamingUrlId)
            this.appStore.displayPageLoading(false)
            this.appStore.displayRightToast(res.status, res.message)
            this.$emit("onDeleteStreamingUrl")
        }
    },
    watch: {
    popupFeedback: {
      handler(newValue, oldValue) {
        if (newValue === true && newValue != oldValue) {
          this.appStore.displayPageLoading(true)
          setTimeout(() => {
            this.appStore.displayPageLoading(false)
            this.appStore.popupCallBack()
          }, 1000)
        }
      },
    },
  }
}
</script>