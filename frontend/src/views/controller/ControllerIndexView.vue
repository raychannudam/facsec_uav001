<template>
    <div class="w-full grid grid-cols-12 gap-3">
        <div class="col-span-8">
            <LiveStreamView :key="triggerConfigUpdate"></LiveStreamView>
        </div>
        <div class="col-span-4">
            <ConfigurationView @onUpdate="updateConfig"></ConfigurationView>
        </div>
        <div class="col-span-12">
            <ControlPanelView></ControlPanelView>
        </div>
    </div>
</template>
<script>
import ConfigurationView from './ConfigurationView.vue';
import ControlPanelView from './ControlPanelView.vue';
import LiveStreamView from './LiveStreamView.vue';
import { initFlowbite } from 'flowbite';

export default {
    components:{
        LiveStreamView,
        ConfigurationView,
        ControlPanelView
    },
    mounted(){
        initFlowbite();
    },
    data(){
        return{
            triggerConfigUpdate: 0
        }
    },
    methods:{
        updateConfig(){
            this.triggerConfigUpdate = this.triggerConfigUpdate + 1
        }
    }
}
</script>