<script setup lang="ts">
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue';

const props = defineProps<{
  track: object
}>()

const track = ref(props.track)

console.log('track', track)

</script>

<template>
  <div class="card">
    <div class="card-content">
      <div class="media">
        <div v-if="track.album.cover" class="media-left">
          <figure class="image is-48x48">
            <img :src="track.album.cover" alt="Playlist image" />
          </figure>
        </div>
        <div class="media-content">
          <p class="title is-4">
            <a :href="track.link" target="_blank" rel="noopener noreferrer">{{
              track.title_short
            }}</a>
          </p>
          <p class="subtitle is-6">{{ track.artist.name }} - {{ track.album.title }}</p>
        </div>
      </div>
      <div class="content"></div>
      <br />
      <nav class="level is-mobile">
        <div v-if="track.preview" class="level-left">
          <slot />

          <a class="level-item"></a>
        </div>
      </nav>
    </div>
  </div>
</template>
