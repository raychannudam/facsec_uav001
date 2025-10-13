<template>
    <PopupModalComponent :id="'streaming-reset-pass-popup-modal-detail' + data.id" @onSave="updateClient(data.id)">
        <template v-slot:header>
            <div>
                <p class="text-xs">Reset Password Streaming client name <span class="block text-xl font-bold">{{ data.name }}</span>
                </p>
            </div>
        </template>
        <template v-slot:body>
            <div class="flex flex-col space-y-3">
                <div class="relative">
                    <input type="text" id="resetCode" v-model="resetCode"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " />
                        <p class="text-xs py-3 italic text-green-600" v-if="resetCodeStatus == 'success'">* {{ resetCodeMessage }}</p>
                        <p class="text-xs py-3 italic text-blue-500 animate-pulse" v-if="resetCodeStatus == 'loading'">* {{ resetCodeMessage }}</p>
                        <p class="text-xs py-3 italic text-red-500" v-if="resetCodeStatus == 'fail'">* {{ resetCodeMessage }}</p>
                    <label for="resetCode"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Reset Code </label>
                </div>
                <div class="relative">
                    <input type="password" id="newPassword" v-model="newPassword"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " />
                    <label for="newPassword"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">New Password</label>
                </div>
                <div class="relative">
                    <input type="password" id="confirmPassword" v-model="confirmPassword"
                        class="block rounded-t-lg px-2.5 pb-2.5 pt-5 w-full text-sm text-gray-900 bg-gray-50 dark:bg-gray-700 border-0 border-b-2 border-gray-300 appearance-none dark:text-white dark:border-gray-600 dark:focus:border-blue-500 focus:outline-none focus:ring-0 focus:border-blue-600 peer"
                        placeholder=" " />
                    <label for="confirmPassword"
                        class="absolute text-sm text-gray-500 dark:text-gray-400 duration-300 transform -translate-y-4 scale-75 top-4 z-10 origin-[0] start-2.5 peer-focus:text-blue-600 peer-focus:dark:text-blue-500 peer-placeholder-shown:scale-100 peer-placeholder-shown:translate-y-0 peer-focus:scale-75 peer-focus:-translate-y-4 rtl:peer-focus:translate-x-1/4 rtl:peer-focus:left-auto">Confrim New Password</label>
                </div>
                <div>
                    <p class="text-xs text-green-600 italic" v-if="validationPasswordStatus == 'success'"> {{ validationPasswordMessage }}</p>
                    <p class="text-xs text-red-500 italic" v-else> {{ validationPasswordMessage }}</p>
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
        PopupModalComponent,
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
            resetCode: "",
            resetCodeMessage: "Sending reset code to your email...",
            validationPasswordStatus: "",
            validationPasswordMessage: "",
            resetCodeStatus: "loading",
            newPassword: "",
            confirmPassword: "",
        }
    },
    methods:{
        async updateClient(id){
            if (this.newPassword != this.confirmPassword){
                this.appStore.displayRightToast("fail", "Please validate your password again!")
                return 
            }
            let data = {
                new_password: this.newPassword,
                validation_code: this.resetCode
            }
            this.appStore.displayPageLoading(true);
            let res = await this.settingStore.updateStreamingClientPassword(id, data);
            this.appStore.displayPageLoading(false);
            this.appStore.displayRightToast(res.status, res.message);
            if (res.status == "success"){
                this.resetForm();
            }

        },
        async requestResetCode(){
            let res = await this.settingStore.requestValidationCode(this.data.id);
            this.resetCodeMessage = res.message;
            this.resetCodeStatus = res.status;
        },
        updateClientModalClosed(){
            this.$emit("onClose")
        },
        resetForm(){
            this.resetCode = ""
            this.newPassword = ""
            this.confirmPassword = ""
        }
    },
    async mounted(){
        await this.requestResetCode()
    },
    watch:{
        newPassword:{
            handler(newVal, oldVal){
                if (newVal!= this.confirmPassword){
                    this.validationPasswordMessage = "Password is not matched!"
                    this.validationPasswordStatus = "fail"
                }else{
                    this.validationPasswordMessage = "Password is matched!"
                    this.validationPasswordStatus = "success"
                }

                if(newVal == ""){
                    this.validationPasswordStatus = ""
                    this.validationPasswordMessage = ""
                }
            }
        },
        confirmPassword:{
            handler(newVal, oldVal){
                if (newVal!= this.newPassword){
                    this.validationPasswordMessage = "Password is not matched!"
                    this.validationPasswordStatus = "fail"
                }else{
                    this.validationPasswordMessage = "Password is matched!"
                    this.validationPasswordStatus = "success"
                }
                if(newVal == ""){
                    this.validationPasswordStatus = ""
                    this.validationPasswordMessage = ""
                }
            }
        }
    }
}
</script>