<template>
  <div class="lg:px-24 space-y-4 py-6">
    <!--Navigation bar-->
    <div class="flex w-full max-w-sm items-center space-x-2">
      <Input
        placeholder="Enter a track to compose from ..."
        v-model="track_id"
        @input="handle_input"
      />

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
import { backend_instance, toast_error, type Track } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { defineProps, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'

const props = defineProps({
  track_id: String,
  preview_url: String,
})

const loading = ref<boolean>(false)

const track_id = ref(props.track_id)

const route = useRoute()

const tracks = ref([] as Track[])

const preview_track = ref<Track | null>(null)

watch(
  () => route.params.id,
  async () => {
    if (track_id.value) {
      await fetch_track_preview(track_id.value)
    }
  },
  { immediate: true },
)

function handle_input(event: InputEvent) {
  preview_track.value = null
  tracks.value = []

  const target = event.target as HTMLInputElement
  const track_id = target.value

  fetch_track_preview(track_id)
}

async function fetch_track_preview(track_id: string) {
  const track = await backend_instance.get_track(track_id).catch(toast_error)
  preview_track.value = track || null
}

async function fetch_tracks() {
  if (!track_id.value) {
    toast.info('Please enter a track id')
    return
  }

  loading.value = true

  // Clear the tracks
  tracks.value = []

  toast.info('Composing tracks ...')

  const response = await backend_instance.compose(track_id.value).catch(toast_error)

  if (!response) {
    loading.value = false
    return
  }

  for (const track_id of response) {
    backend_instance
      .get_track(track_id)
      .catch(toast_error)
      .then((result) => {
        if (result) {
          tracks.value.push(result)
        }
      })
  }

  loading.value = false
}

function compose() {
  fetch_tracks()
}
</script>
