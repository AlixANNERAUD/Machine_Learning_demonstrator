<template>
  <div class="lg:px-24">
    <!--Navigation bar-->
    <div class="flex w-full max-w-sm gap-2 items-center py-4">
      <Input class="input" type="text" placeholder="Find a track on Deezer" @input="fetch_data" />
    </div>
    <!--Table-->
    <TracksTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import TracksTableComponent from '@/components/TracksTableComponent.vue'
import Input from '@/components/ui/input/Input.vue'
import { backend, toast_error } from '@/stores/backend'
import { ref } from 'vue'

const tracks = ref([])

async function fetch_data(event: InputEvent) {
  tracks.value = []

  const target = event.target as HTMLInputElement
  const query = target.value

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
