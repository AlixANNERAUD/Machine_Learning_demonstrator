<template>
  <div class="px-96">
    <!--Navigation bar-->
    <div class="flex gap-2 items-center py-4">
      <Input
        class="input"
        type="text"
        placeholder="Find a track on Deezer"
        @input="fetch_data"
      />
    </div>
    <!--Table-->
    <MusicTableComponent v-if="tracks.length" class="w-full" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import MusicTableComponent from '@/components/TracksTableComponent.vue'
import Input from '@/components/ui/input/Input.vue'
import { backend, toast_error } from '@/stores/backend'
import { ref } from 'vue'

const tracks = ref([])

async function fetch_data(event : InputEvent) {
  tracks.value = []

  const search = event.target as HTMLInputElement
  const query = search.value

  console.log('query', query)

  if (!query) {
    return
  }

  const result = await backend
    .get('/deezer/search', {
      params: {
        query: query,
      },
    })
    .catch(toast_error)

  if (!result || !result.data.data) {
    return
  }

  tracks.value = result.data.data

  console.log('tracks', tracks.value)
}
</script>
