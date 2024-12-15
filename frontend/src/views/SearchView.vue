<template>
  <div class="lg:px-24 py-6">
    <!--Navigation bar-->
    <div class="relative w-full max-w-sm items-center py-4">
      <Input class="pl-10" type="text" placeholder="Find a track on Deezer" @input="fetch_data" />

      <span class="absolute start-0 inset-y-0 flex items-center justify-center px-4">
        <FontAwesomeIcon :icon="fas.faSearch" />
      </span>
    </div>
    <!--Table-->
    <TracksTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import TracksTableComponent from '@/components/TracksTableComponent.vue'
import Input from '@/components/ui/input/Input.vue'
import { backend_instance, toast_error, type Track } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue'

const tracks = ref<Track[]>([])

async function fetch_data(event: InputEvent) {
  tracks.value = []

  const target = event.target as HTMLInputElement
  const query = target.value

  if (!query) {
    return
  }

  const response = await backend_instance.search_deezer(query).catch(toast_error)

  if (!response) {
    return
  }

  tracks.value = response
}
</script>
