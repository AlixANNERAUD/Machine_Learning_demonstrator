<template>
  <HeroComponent title="Compose" subtitle="Find matches">
    <div class="field has-addons">
      <p class="control">
        <input class="input" type="text" placeholder="Find a track" v-model="track_id" />
      </p>
      <p class="control">
        <button class="button" @click="compose">
          <FontAwesomeIcon :icon="fas.faWandMagicSparkles" /> Compose
        </button>
      </p>
    </div>

    <div v-if="loading" class="skeleton-block"></div>
  </HeroComponent>
  <ErrorModalComponent v-if="error" :message="error" />
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'
import HeroComponent from '@/components/HeroComponent.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import axiosInstance from '@/stores/axiosInstance'
import get_spotify from '@/stores/spotifyInstance'
import ErrorModalComponent from '@/components/ErrorModalComponent.vue'

const props = defineProps({
  track_id: String,
})

const loading = ref<boolean>(false)
const error = ref<string | null>(null)

const track_id = ref(props.track_id)

const tracks = ref([])

async function fetch_data() {
  loading.value = true

  const spotify = await get_spotify()

  if (!track_id.value) {
    loading.value = false
    return
  }

  const track = await spotify.tracks.get(track_id.value)

  console.log('preview_url', track.preview_url)

  const result = axiosInstance.get('/compose', {
    params: {
      track_id: track_id.value,
      preview_url: track.preview_url,
    },
  })

  tracks.value = (await result).data

  loading.value = false
}

function compose() {
  console.log('ComposeView : compose')
  fetch_data()
}
</script>
