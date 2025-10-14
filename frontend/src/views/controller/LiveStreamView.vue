<template>
    <div class="flex flex-col space-y-3">
        <div class="text-2xl font-bold flex items-center space-x-3">
            <span class="text-2xl material-symbols-outlined">
                camera_video
            </span>
            <p>Live Streams</p>
        </div>
        <p class="text-gray-600 dark:text-gray-400">Get real-time live stream video from the cameras on the
            drone.</p>
        <hr class="border-0.5 border-gray-200">
        <div class="grid grid-cols-12 gap-3 h-[50vh] w-full">
            <div class="col-span-8 bg-gray-500 rounded-md flex items-center justify-center space-x-3 w-full h-full">
                <span class="material-symbols-outlined animate-pulse">
                    videocam
                </span>
                <p class="animate-pulse">CAM 01</p>
            </div>
            <div class="col-span-4">
                <div class="grid grid-rows-3 gap-3 w-full h-full">
                    <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 ">
                        <span class="material-symbols-outlined animate-pulse">
                            videocam
                        </span>
                        <p class="animate-pulse">CAM 02</p>
                    </div>
                    <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 ">
                        <span class="material-symbols-outlined animate-pulse">
                            videocam
                        </span>
                        <p class="animate-pulse">CAM 03</p>
                    </div>
                    <div class="bg-gray-500 rounded-md flex items-center justify-center space-x-3 ">
                        <span class="material-symbols-outlined animate-pulse">
                            videocam
                        </span>
                        <p class="animate-pulse">CAM 04</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>