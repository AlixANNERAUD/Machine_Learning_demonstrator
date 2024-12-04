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

    <div class="grid is-col-min-10">
      <div v-for="track in tracks" :key="track.id" class="cell card">
        <div class="card-content">
          <div class="media">
            <div v-if="track.album.images[0]" class="media-left">
              <figure class="image is-48x48">
                <img :src="track.album.images[0].url" alt="Playlist image" />
              </figure>
            </div>
            <div class="media-content">
              <p class="title is-4">
                <a :href="track.external_urls.spotify" target="_blank" rel="noopener noreferrer">{{
                  track.name
                }}</a>
              </p>
              <p class="subtitle is-6">{{ track.artists[0].name }} - {{ track.album.name }}</p>
            </div>
          </div>
          <div class="content"></div>
          <br />
          <nav class="level is-mobile">
            <div v-if="track.preview_url" class="level-left">
              <router-link :to="{ name: 'Compose', params: { track_id: track.id } }">
                <span class="icon is-small">
                  <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
                </span>
              </router-link>
              <a class="level-item"> </a>
            </div>
          </nav>
        </div>
      </div>
    </div>
  </HeroComponent>
</template>

<script setup lang="ts">
import HeroComponent from '@/components/HeroComponent.vue'
import get_spotify from '@/stores/spotifyInstance'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import type { Track } from '@spotify/web-api-ts-sdk'
import { ref } from 'vue'

const search = ref('')

const tracks = ref<Track[]>([])

async function fetch_data() {
  const spotify = await get_spotify()

  const result = await spotify.search(search.value, ['track'], 'US', 10)

  console.log('result', result)

  tracks.value = result.tracks.items
}

function search_track() {
  fetch_data()
}
</script>
