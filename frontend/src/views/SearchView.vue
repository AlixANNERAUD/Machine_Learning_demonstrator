<template>
  <div class="px-44">
    <!--Navigation bar-->
    <div class="flex gap-2 items-center py-4">
      <Input class="input" type="text" placeholder="Find a track on Deezer" v-model="search" @input="search_track" />
    </div>
    <!--Table-->
    <MusicTableComponent v-if="tracks.length" class="w-full" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import MusicTableComponent from '@/components/TracksTableComponent.vue'
import Input from '@/components/ui/input/Input.vue'
import axiosInstance from '@/stores/axiosInstance'
import { ref } from 'vue'

const search = ref('')
const tracks = ref([])

async function fetch_data() {
  if (!search.value) {
    tracks.value = []
    return
  }

  const result = await axiosInstance.get('/deezer/search', {
    params: {
      query: search.value,
    },
  })

  tracks.value = result.data.data

  console.log('tracks', tracks.value)
}

function search_track() {
  fetch_data()
}
</script>
