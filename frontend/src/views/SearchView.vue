<template>
  <HeroComponent title="Search" subtitle="Search for music">
    <div class="field has-addons">
      <p class="control">
        <input class="input" type="text" placeholder="Find a track" v-model="search" />
      </p>
      <p class="control">
        <button class="button" @click="search_track">Search</button>
      </p>
    </div>

    <div class="grid is-col-min-15">
      <div v-for="track in tracks" :key="track.id" class="cell">
        <TrackCardComponent :track="track">
          <router-link
            :to="{
              name: 'Compose',
              params: { track_id: track.id, preview_url: track.preview },
            }"
          >
            <span class="icon is-small">
              <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
            </span>
          </router-link>
        </TrackCardComponent>
      </div>
    </div>
  </HeroComponent>
</template>

<script setup lang="ts">
import HeroComponent from '@/components/HeroComponent.vue'
import TrackCardComponent from '@/components/TrackCardComponent.vue'
import axiosInstance from '@/stores/axiosInstance'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue'

const search = ref('')

const tracks = ref([])

async function fetch_data() {
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
