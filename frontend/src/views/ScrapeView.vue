<template>
  <HeroComponent title="Scrape" subtitle="Scrape playlist from Deezer">
    <!--Columns-->
    <div class="columns">
      <!--First column : scraping-->
      <div class="column">
        <div class="field has-addons">
          <p class="control">
            <input class="input" type="text" placeholder="Playlist identifier" v-model="playlist_id" />
          </p>
          <p class="control">
            <button class="button" @click="scrape">
              <FontAwesomeIcon :icon="fas.faCloudArrowDown" /> Scrape
            </button>
          </p>
        </div>

        <div class="grid is-col-min-15">
          <div v-for="track in tracks" :key="track.id" class="cell">
            <TrackCardComponent :track="track" />
          </div>
        </div>

        <div v-if="loading" class="skeleton-block"></div>
      </div>
      <!--Second column : queue-->
      <div class="column">

        <table class="table is-fullwidth">
          <thead>
            <tr>
              <th>Track</th>
              <th>Artist</th>
              <th>Album</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="track in queue" :key="track.id">
              <td>{{ track.title }}</td>
              <td>{{ track.artist }}</td>
              <td>{{ track.album }}</td>
              <td>{{ track.duration }}</td>
            </tr>
          </tbody>
        </table>

      </div>
    </div>
  </HeroComponent>
</template>

<script setup lang="ts">
import HeroComponent from '@/components/HeroComponent.vue'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { ref } from 'vue'

const playlist_id = ref('')

const tracks = ref([])
</script>
