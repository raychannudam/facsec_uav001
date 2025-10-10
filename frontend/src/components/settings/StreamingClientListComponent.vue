<template>
  <div :id="id" data-accordion="collapse" v-if="streamingClientList.length > 0">
    <div v-for="data, index in streamingClientList">
      <h2 :id="'streaming-accordion-collapse-heading-' + index">
        <button v-if="index == 0" type="button"
          class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-0 rounded-t-xl border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
          :data-accordion-target="'#streaming-accordion-collapse-body-' + index" aria-expanded="true"
          :aria-controls="'streaming-accordion-collapse-body-' + index">
          <div class="flex space-x-3 items-center justify-evenly flex-1">
            <p class="text-sm text-start">Name <span class="block font-bold text-xl">{{ data.name }}</span></p>
            <p class="text-sm text-start">Status <span class="block font-bold text-xl text-green-600"
                v-if="data.status">ACTIVE</span> <span class="block font-bold text-xl text-red-600"
                v-else>INACTIVE</span></p>
            <p class="text-sm text-start">Description <span class="block font-bold text-xl">{{ data.description
                }}</span>
            </p>
            <p class="text-sm text-start">Last Modified <span class="block font-bold text-xl">{{ data.updated_at
                }}</span></p>
          </div>
          <svg data-accordion-icon class="w-3 h-3 rotate-180 shrink-0" aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5 5 1 1 5" />
          </svg>
        </button>
        <button v-else type="button"
          class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-1 rounded-t-none border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
          :data-accordion-target="'#streaming-accordion-collapse-body-' + index" aria-expanded="true"
          :aria-controls="'streaming-accordion-collapse-body-' + index">
          <div class="flex space-x-3 items-center justify-evenly flex-1">
            <p class="text-sm text-start">Name <span class="block font-bold text-xl">{{ data.name }}</span></p>
            <p class="text-sm text-start">Status <span class="block font-bold text-xl text-green-600"
                v-if="data.status">ACTIVE</span> <span class="block font-bold text-xl text-red-600 px-3 rounded-md"
                v-else>INACTIVE</span></p>
            <p class="text-sm text-start">Description <span class="block font-bold text-xl">{{ data.description
                }}</span>
            </p>
            <p class="text-sm text-start">Last Modified <span class="block font-bold text-xl">{{ data.updated_at
                }}</span></p>
          </div>
          <svg data-accordion-icon class="w-3 h-3 rotate-180 shrink-0" aria-hidden="true"
            xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
            <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
              d="M9 5 5 1 1 5" />
          </svg>
        </button>
      </h2>
      <div :id="'streaming-accordion-collapse-body-' + index" class="hidden"
        :aria-labelledby="'streaming-accordion-collapse-heading-' + index">
        <div
          class="p-5 border border-b-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900 flex flex-col space-y-3">
          <!-- Client Info -->
          <div class="flex items-end justify-start space-x-3">
            <p class="text-xs max-w-max">USERNAME <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> {{ data.username }} </code>
            </p>
            <p class="text-xs max-w-max">PASSWORD <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> ***** </code>
            </p>
            <p class="text-xs max-w-max">ACTIONS <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> {{ data.config["actions"] }} </code>
            </p>
            <button type="button" :data-modal-target="'streaming-reset-pass-popup-modal-detail' + data.id" :data-modal-toggle="'streaming-reset-pass-popup-modal-detail' + data.id"
              class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
              <span class="material-symbols-outlined">
                key
              </span>
              <p>Reset password</p>
            </button>
            <button type="button" :data-modal-target="'streaming-popup-modal-detail' + data.id"
              :data-modal-toggle="'streaming-popup-modal-detail' + data.id"
              class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:outline-none focus:ring-yellow-300 rounded-lg text-center dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800">
              <span class="material-symbols-outlined">
                edit_note
              </span>
              <p>Edit client</p>
            </button>
            <button type="button" :data-modal-target="'delete_streaming_client_confirm_popup'+data.id"
              :data-modal-toggle="'delete_streaming_client_confirm_popup'+data.id" @click="displayStreamingClientDeleteConfirmPopup(data.id)"
            class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">
              <span class="material-symbols-outlined">
                delete_forever
              </span>
              <p>Delete client</p>
            </button>
            <StreamingClientResetPasswordComponent  v-if="data" :data="data"></StreamingClientResetPasswordComponent>
            <StreamingClientUpdateComponent v-if="data" :data="data" @onClose="streamingClientEditModalClosed"></StreamingClientUpdateComponent>
            <ConfirmPopupModelComponent :model_id="'delete_streaming_client_confirm_popup'+data.id"></ConfirmPopupModelComponent>
          </div>
          <div>
            <hr class="border-0.5 border-dashed">
          </div>
          <!-- URL Info -->
           <div class="flex items-center justify-start space-x-3 ">
            <StreamingUrlCreateFormComponent :streamingClientData="data" @onSubmit="createStreamingUrl"></StreamingUrlCreateFormComponent>
            <div class="flex-1 flex justify-end">
              <form class="max-w-md w-full">
                <label for="streamingUrlQuery"
                  class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                <div class="relative">
                  <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                    </svg>
                  </div>
                  <input type="search" id="streamingUrlQuery" v-model="streamingUrlQuery"
                    class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Search url ..." required />
                  <button type="submit"
                    class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
                </div>
              </form>
            </div>
          </div>
          <div>
            <StreamingUrlTableComponent @onDeleteStreamingUrl="streamingURLDeleted" :allStreamingUrls="allStreamingUrls[data.id]"></StreamingUrlTableComponent>
            <!-- {{ allStreamingUrls }} -->
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
import { initFlowbite } from 'flowbite';
import { storeToRefs } from 'pinia';
import ConfirmPopupModelComponent from '../utils/ConfirmPopupModelComponent.vue';
import StreamingClientUpdateComponent from './StreamingClientUpdateComponent.vue';
import StreamingClientResetPasswordComponent from './StreamingClientResetPasswordComponent.vue';
import StreamingUrlCreateFormComponent from './StreamingUrlCreateFormComponent.vue';
import StreamingUrlTableComponent from './StreamingUrlTableComponent.vue';
export default {
  name: "StreamingClientListComponent",
  // props: ['streamingClientList', 'id'],
  props: {
    streamingClientList: {
      type: Array,
      default: []
    },
    id: String
  },
  components: {
    ConfirmPopupModelComponent,
    StreamingClientUpdateComponent,
    StreamingClientResetPasswordComponent,
    StreamingUrlCreateFormComponent,
    StreamingUrlTableComponent
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
  data() {
    return {
      toDeleteStreamingClient: undefined,
      streamingUrlQuery: "",
      allStreamingUrls: {}
    }
  },
  async mounted() {
    initFlowbite();
    await this.getAllStreamingUrl();
  },
  methods: {
    displayStreamingClientDeleteConfirmPopup(id){
      this.toDeleteStreamingClient = id
      this.appStore.displayConfirmPopupModel("Are you sure to delete this client?", this.deleteStreamingClient)
    },
    async deleteStreamingClient(){
      if (this.toDeleteStreamingClient != undefined){
        this.appStore.displayPageLoading(true)
        let res = await this.settingStore.deleteStreamingClient(this.toDeleteStreamingClient)
        this.appStore.displayPageLoading(false)
        this.appStore.displayRightToast(res.status, res.message);
        this.$emit("onCompletedDeleteStreamingClient")
      }
    },
    streamingClientEditModalClosed(){
      this.$emit("onStreamingClientEditModalClose")
    },
    async createStreamingUrl(data){
      this.appStore.displayPageLoading(true);
      let res = await this.settingStore.crateStreamingUrl(data);
      this.appStore.displayPageLoading(false);
      this.appStore.displayRightToast(res.status, res.message)
      await this.getAllStreamingUrl();
    },
    async getAllStreamingUrl(){
      this.streamingClientList.forEach(async item=>{
        let res = await this.settingStore.getAllStreamingUrls(item.id);
        if (res.status == "success"){
          this.allStreamingUrls[item.id] = res.data
        }
      })
    },
    async streamingURLDeleted(){
      await this.getAllStreamingUrl();
    }
  },
  watch: {
    popupFeedback: {
      handler(newValue, oldValue) {
        if (newValue === true) {
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