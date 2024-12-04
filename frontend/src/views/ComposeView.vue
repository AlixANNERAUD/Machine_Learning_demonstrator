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

    <div class="grid is-col-min-15">
      <div v-for="track in tracks" :key="track.id" class="cell">
        <TrackCardComponent :track="track" />
      </div>
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
import ErrorModalComponent from '@/components/ErrorModalComponent.vue'
import TrackCardComponent from '@/components/TrackCardComponent.vue'

const props = defineProps({
  track_id: String,
  preview_url: String,
})

const loading = ref<boolean>(false)
const error = ref<string | null>(null)

const track_id = ref(props.track_id)

const tracks = ref([])

async function fetch_data() {
  loading.value = true

  // Clear the tracks
  tracks.value = []

  console.log('props.preview_url', props.preview_url)

  const result = axiosInstance.get('/compose', {
    params: {
      track_id: track_id.value,
      preview_url: props.preview_url,
    },
  })

  const tracks_id = (await result).data.similar_tracks

  for (const track_id of tracks_id) {
    axiosInstance
      .get(`/deezer/track`, {
        params: {
          track_id,
        },
      })
      .then((result) => {
        console.log('result', result.data)

        tracks.value.push(result.data)
      })
  }

  loading.value = false
}

function compose() {
  console.log('ComposeView : compose')
  fetch_data()
}
</script>
