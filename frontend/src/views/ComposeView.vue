<template>
  <div class="lg:px-24 space-y-4">
    <!--Navigation bar-->
    <div class="flex w-full max-w-sm items-center space-x-2">
      <Input placeholder="Enter a track to compose from ..." v-model="track_id" @input="handle_input" />

      <Button @click="compose">
        <FontAwesomeIcon :icon="fas.faWandMagicSparkles" /> Compose
      </Button>
    </div>
    <!--Preview track table-->
    <TracksTableComponent v-if="preview_track" :tracks="[preview_track]" />
    <!--Result track table-->
    <TracksTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import TracksTableComponent from '@/components/TracksTableComponent.vue'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import { backend, backend_instance, toast_error } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { defineProps, ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const props = defineProps({
  track_id: String,
  preview_url: String,
})

const loading = ref<boolean>(false)

const track_id = ref(props.track_id)

const route = useRoute()


watch(() => route.params.id, async () => {
  if (track_id.value) {
    await fetch_track_preview(track_id.value)
  }
}, { immediate: true })

const tracks = ref([])

const preview_track = ref<object | null>(null)


function handle_input(event: InputEvent) {
  preview_track.value = null
  tracks.value = []

  const target = event.target as HTMLInputElement
  const track_id = target.value

  fetch_track_preview(track_id)
}

async function fetch_track_preview(track_id: string) {
  preview_track.value = await backend_instance.get_track(track_id).catch(toast_error)
}

async function fetch_tracks() {
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
      timeout: 30000,
    },
    )
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
  fetch_tracks()
}
</script>
