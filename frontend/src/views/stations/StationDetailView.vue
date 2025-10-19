<template>
    <div class="flex flex-col space-y-3" v-if="stationData">
        <div class="flex flex-row space-x-3">
            <div>
                <p class="font-bold text-xl px-3 border-l-4">Station Details</p>
            </div>
        </div>
        <div class="flex flex-row space-x-3 items-center justify-evenly">
            <div>
                <p class="text-xs">Station name <span class="block font-bold text-base">{{ stationData.name }}</span>
                </p>
            </div>
            <div>
                <p class="text-xs">Station description <span class="block font-bold text-base">{{
                        stationData.description }}</span> </p>
            </div>
            <div>
                <p class="text-xs">Station lat & lng <span class="block font-bold text-base">{{ stationData.lat }}, {{
                        stationData.long }}</span> </p>
            </div>
        </div>
    </div>
    <div class="flex flex-col space-y-3 items-center justify-center w-full p-3 opacity-50" v-else>
        <span class="material-symbols-outlined text-6xl">
            left_click
        </span>
        <p class="text-center italic">Click on station icon to see the details</p>
    </div>
</template>
<script>
export default {
    props: {
        stationData: {
            type: Object
        }
    }
}
</script>