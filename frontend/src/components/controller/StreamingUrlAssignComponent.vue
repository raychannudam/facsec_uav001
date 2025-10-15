<template>
  <div class="flex flex-row space-x-3 items-center justify-start relative">
    <p class="text-sm">{{ name }}</p>
    <button :id="id + 'Button'" :data-dropdown-toggle="id" data-dropdown-placement="bottom"
      class="text-white focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center inline-flex items-center flex-1 dark:focus:ring-blue-800 border border-blue-600 shadow-blue-50"
      type="button">
      <p class="flex-1 start">{{ dropDownDesc }}</p>
      <svg class="w-2.5 h-2.5 ms-3" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 10 6">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m1 1 4 4 4-4" />
      </svg>
    </button>
    <!-- Dropdown menu -->
    <div :id="id" class="z-10 hidden bg-white rounded-lg shadow-sm w-full dark:bg-gray-700">
      <div class="p-3">
        <label :for="'search' + id" class="sr-only">Search</label>
        <div class="relative">
          <div class="absolute inset-y-0 rtl:inset-r-0 start-0 flex items-center ps-3 pointer-events-none">
            <svg class="w-4 h-4 text-gray-500 dark:text-gray-400" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 20 20">
              <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="m19 19-4-4m0-7A7 7 0 1 1 1 8a7 7 0 0 1 14 0Z" />
            </svg>
          </div>
          <input type="text" :id="'search' + id" v-model="query"
            class="block w-full p-2 ps-10 text-sm text-gray-900 border border-gray-300 rounded-lg bg-gray-50 focus:ring-blue-500 focus:border-blue-500 dark:bg-gray-600 dark:border-gray-500 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
            placeholder="Search streaming url...">
        </div>
      </div>
      <ul class="h-48 px-3 pb-3 overflow-y-auto text-sm text-gray-700 dark:text-gray-200" :aria-labelledby="id + 'Button'">
        <li>
          <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
            <input :id="'checkbox-item-' + id + '-1'" type="radio" value="url1" v-model="selectedUrl"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
            <label :for="'checkbox-item-' + id + '-1'"
              class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">URL 1</label>
          </div>
        </li>
        <li>
          <div class="flex items-center ps-2 rounded-sm hover:bg-gray-100 dark:hover:bg-gray-600">
            <input :id="'checkbox-item-' + id + '-2'" type="radio" value="url2" v-model="selectedUrl"
              class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded-sm focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-700 dark:focus:ring-offset-gray-700 focus:ring-2 dark:bg-gray-600 dark:border-gray-500">
            <label :for="'checkbox-item-' + id + '-2'"
              class="w-full py-2 ms-2 text-sm font-medium text-gray-900 rounded-sm dark:text-gray-300">URL 2</label>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<script>
export default {
  name: 'StreamingUrlAssignComponent',
  props: ['id', 'name', 'dropDownDesc'],
  data() {
    return {
      query: '',
      selectedUrl: ''
    }
  },
  methods: {
    urlSelected() {
      this.$emit('onUrlSelect', {
        id: this.id,
        name: this.name,
        url: this.selectedUrl
      })
    }
  },
  watch: {
    selectedUrl(newVal, oldVal) {
      if (newVal !== oldVal) {
        this.urlSelected();
      }
    }
  }
}
</script>
