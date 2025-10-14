<template>
    <div class="w-full grid grid-cols-12 gap-3">
        <div class="col-span-8">
            <LiveStreamView></LiveStreamView>
        </div>
        <div class="col-span-4">
            <ConfigurationView></ConfigurationView>
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

export default {
    components:{
        LiveStreamView,
        ConfigurationView,
        ControlPanelView
    }
}
</script>