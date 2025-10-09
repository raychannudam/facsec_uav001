<template>
  <div :id="id" data-accordion="collapse" v-if="mqttClientList.length > 0">
    <div v-for="data, index in mqttClientList">
      <h2 :id="'accordion-collapse-heading-' + index">
        <button v-if="index == 0" type="button"
          class="flex items-center justify-between w-full p-5 font-medium rtl:text-right text-gray-500 border border-b-0 rounded-t-xl border-gray-200 focus:ring-4 focus:ring-gray-200 dark:focus:ring-gray-800 dark:border-gray-700 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 gap-3"
          :data-accordion-target="'#accordion-collapse-body-' + index" aria-expanded="true"
          :aria-controls="'accordion-collapse-body-' + index">
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
          :data-accordion-target="'#accordion-collapse-body-' + index" aria-expanded="true"
          :aria-controls="'accordion-collapse-body-' + index">
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
      <div :id="'accordion-collapse-body-' + index" class="hidden"
        :aria-labelledby="'accordion-collapse-heading-' + index">
        <div
          class="p-5 border border-b-0 border-gray-200 dark:border-gray-700 dark:bg-gray-900 flex flex-col space-y-3">
          <!-- Client Info -->
          <div class="flex items-end justify-start space-x-3">
            <p class="text-xs max-w-max">PROTOCOL <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> MQTTS </code>
            </p>
            <p class="text-xs max-w-max">HOST <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> mqtt-broker.aitips.digital </code>
            </p>
            <p class="text-xs max-w-max">PORT <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> 8883 </code>
            </p>
            <p class="text-xs max-w-max">USERNAME <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> {{ data.username }} </code>
            </p>
            <p class="text-xs max-w-max">PASSWORD <code
                class=" block p-1 px-2 rounded-md dark:bg-gray-600 bg-gray-300 font-bold text-base"> ***** </code>
            </p>
            <button type="button"
              class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 rounded-lg text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">
              <span class="material-symbols-outlined">
                key
              </span>
              <p>Reset password</p>
            </button>
            <button type="button" :data-modal-target="'popup-modal-detail' + data.id"
              :data-modal-toggle="'popup-modal-detail' + data.id"
              class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-yellow-700 hover:bg-yellow-800 focus:ring-4 focus:outline-none focus:ring-yellow-300 rounded-lg text-center dark:bg-yellow-600 dark:hover:bg-yellow-700 dark:focus:ring-yellow-800">
              <span class="material-symbols-outlined">
                edit_note
              </span>
              <p>Edit client</p>
            </button>
            <button type="button" @click="displayMqttClientDeleteComfirmPopup(data.id)"
              :data-modal-target="'delete_mqtt_client_confirm_popup' + data.id"
              :data-modal-toggle="'delete_mqtt_client_confirm_popup' + data.id"
              class="px-5 py-1 text-sm font-medium text-white inline-flex items-center space-x-2 bg-red-700 hover:bg-red-800 focus:ring-4 focus:outline-none focus:ring-red-300 rounded-lg text-center dark:bg-red-600 dark:hover:bg-red-700 dark:focus:ring-red-800">
              <span class="material-symbols-outlined">
                delete_forever
              </span>
              <p>Delete client</p>
            </button>
            <MqtqClientUpdateComponent v-if="data" :data="data" @onClose="mqttClientEditModalClosed"></MqtqClientUpdateComponent>
            <ConfirmPopupModelComponent :model_id="'delete_mqtt_client_confirm_popup' + data.id">
            </ConfirmPopupModelComponent>
          </div>
          <div>
            <hr class="border-0.5 border-dashed">
          </div>
          <!-- Topic Info -->
          <div class="flex items-center justify-start space-x-3 ">
            <MqttTopicCreateFormComponent :mqttClientData="data" @onSubmit="createMqttTopic">
            </MqttTopicCreateFormComponent>
            <div class="flex-1 flex justify-end">
              <form class="max-w-md w-full">
                <label for="mqttTopicQuery"
                  class="mb-2 text-sm font-medium text-gray-900 sr-only dark:text-white">Search</label>
                <div class="relative">
                  <div class="absolute inset-y-0 start-0 flex items-center ps-3 pointer-events-none">
                    <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true"
                      xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
                      <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                        d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
                    </svg>
                  </div>
                  <input type="search" id="mqttTopicQuery" v-model="mqttTopicQuery"
                    class="block w-full p-4 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
                    placeholder="Search path, payload, config ..." required />
                  <button type="submit"
                    class="text-white absolute end-2.5 bottom-2.5 bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Search</button>
                </div>
              </form>
            </div>
          </div>
          <div>
            <MqttTopicTableComponent :allMqttTopic="allMqttTopic[data.id]"></MqttTopicTableComponent>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import MqttTopicTableComponent from './MqttTopicTableComponent.vue';
import MqttTopicCreateFormComponent from './MqttTopicCreateFormComponent.vue';
import ConfirmPopupModelComponent from '../utils/ConfirmPopupModelComponent.vue';
import MqtqClientUpdateComponent from '@/components/settings/MqttClientUpdateComponent.vue';
import { useAppStore } from '@/stores/AppStore';
import { useSettingStore } from '@/stores/SettingStore';
import { initFlowbite } from 'flowbite';
import { storeToRefs } from 'pinia';
export default {
  name: "MqttClientListComponent",
  // props: ['mqttClientList', 'id'],
  props: {
    mqttClientList: {
      type: Array,
      default: []
    },
    id: String
  },
  components: {
    MqttTopicTableComponent,
    MqttTopicCreateFormComponent,
    ConfirmPopupModelComponent,
    MqtqClientUpdateComponent,
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
      toDeleteMqttClientId: undefined,
      allMqttTopic: {},
      mqttTopicQuery: ""
    }
  },
  async mounted() {
    initFlowbite();
    await this.getAllMqttTopic();
  },
  methods: {
    displayMqttClientDeleteComfirmPopup(id) {
      this.toDeleteMqttClientId = id
      this.appStore.displayConfirmPopupModel("Are you sure to delete this MQTT client?", this.deleteMqttClient)
    },
    async deleteMqttClient() {
      if (this.toDeleteMqttClientId != undefined) {
        this.appStore.displayPageLoading(true)
        let res = await this.settingStore.deleteMqttClient(this.toDeleteMqttClientId)
        this.appStore.displayPageLoading(false)
        this.appStore.displayRightToast(res.status, res.message);
        this.$emit("onCompletedDeleteMqttClient")
      }
    },
    async mqttClientEditModalClosed() {
      this.$emit("onMqttClientEditModalClose")
    },
    async getAllMqttTopic() {
      this.mqttClientList.forEach(async item => {
        let res = await this.settingStore.getAllMqttTopicByMqttClientId(item.id)
        if (res.status == "success") {
          this.allMqttTopic[item.id] = res.data
        }
      })
    },
    async createMqttTopic(data) {
      this.appStore.displayPageLoading(true);
      let res = await this.settingStore.createMqttTopic(data);
      this.appStore.displayPageLoading(false);
      this.appStore.displayRightToast(res.status, res.message);
      await this.getAllMqttTopic();
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