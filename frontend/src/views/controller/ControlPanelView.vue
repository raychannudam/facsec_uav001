<template>
    <div class="flex flex-col space-y-3">

        <div class="flex flex-row space-x-3 w-full items-end justify-between">
            <div class="text-2xl flex flex-col items-start space-y-3">
                <div class="flex font-bold flex-row space-x-3 items-center">
                    <span class="text-2xl material-symbols-outlined">
                        stadia_controller
                    </span>
                    <p>Control Panel</p>
                </div>
                <p class="text-gray-600 dark:text-gray-400 text-sm">
                    Get real-time live stream video from the cameras on the drone.
                </p>
            </div>
            <div class="flex items-center space-x-3 dark:text-gray-400 px-3">
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        device_thermostat
                    </span>
                    <p>Temp, </p>
                    <p class="font-bold dark:text-white">-- &#8451;</p>
                </div>
                <div>
                    |
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        speed
                    </span>
                    <p>Speed, </p>
                    <p class="font-bold dark:text-white">-- km/h</p>
                </div>
                <div>
                    |
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        altitude
                    </span>
                    <p>Altitude, </p>
                    <p class="font-bold dark:text-white">---- m</p>
                </div>
                <div class="flex items-center space-x-0.5 text-xs p-1 shadow dark:shadow-white/30">
                    <span class="material-symbols-outlined">
                        timer
                    </span>
                    <p>Time, </p>
                    <p class="font-bold dark:text-white">-- mn</p>
                </div>
            </div>
        </div>
        <hr class="border-0.5 border-gray-200">
    </div>
</template>