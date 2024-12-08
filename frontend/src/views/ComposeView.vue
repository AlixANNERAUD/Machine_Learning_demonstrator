<template>
  <div class="px-44">
    <!--Navigation bar-->
    <div class="flex w-full max-w-sm items-center space-x-2 py-4">
      <Input placeholder="Enter a track to compose from ..." v-model="track_id" />

      <Button @click="compose">
        <FontAwesomeIcon :icon="fas.faWandMagicSparkles" /> Compose
      </Button>
    </div>
    <!--Table-->
    <TracksTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import { defineProps, ref } from 'vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { backend, toast_error } from '@/stores/backend'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import TracksTableComponent from '@/components/TracksTableComponent.vue'

const props = defineProps({
  track_id: String,
  preview_url: String,
})

const loading = ref<boolean>(false)

const track_id = ref(props.track_id)

const tracks = ref([])

async function fetch_data() {
  loading.value = true

  // Clear the tracks
  tracks.value = []

  console.log('props.preview_url', props.preview_url)

  const result = await backend
    .get('/compose', {
      params: {
        track_id: track_id.value,
        preview_url: props.preview_url,
      },
    })
    .catch(toast_error)

  const tracks_id = result.data.similar_tracks

  for (const track_id of tracks_id) {
    backend
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
