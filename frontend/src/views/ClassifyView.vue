<template>
  <div class="lg:px-24 space-y-4 py-6">
    <!--Navigation bar-->
    <div class="flex w-full max-w-sm items-center space-x-2">
      <Input
        placeholder="Enter a track to compose from ..."
        v-model="track_id"
        @input="handle_input"
      />

      <Button @click="fetch_classify">
        <FontAwesomeIcon :icon="fas.faLayerGroup" /> Classify
      </Button>
    </div>
    <!--Preview track table-->
    <TracksTableComponent v-if="preview_track" :tracks="[preview_track]" />
    <!--Result genres-->
    <div v-if="genres.length" class="flex flex-wrap gap-4">
      <Card class="w-full" v-for="genre in genres" :key="genre.id">
        <CardHeader>
          <img :src="genre.picture" class="w-24 h-24" alt="genre picture" />
          <CardTitle>{{ genre.name }}</CardTitle>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Card, CardHeader, CardTitle } from '@/components/ui/card'
import TracksTableComponent from '@/components/TracksTableComponent.vue'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import { backend_instance, toast_error, type Track, type Genre } from '@/stores/backend'
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

console.log(props.track_id)

const route = useRoute()

const preview_track = ref<Track | null>(null)

const genres = ref<Genre[]>([])

watch(
  () => route.params.id,
  async () => {
    if (track_id.value) {
      await fetch_track_preview(track_id.value)
    }
  },
  { immediate: true },
)

async function fetch_track_preview(track_id: string) {
  const track = await backend_instance.get_track(track_id).catch(toast_error)
  preview_track.value = track || null
}

function handle_input(event: InputEvent) {
  preview_track.value = null
  genres.value = []

  const target = event.target as HTMLInputElement
  const track_id = target.value

  fetch_track_preview(track_id)
}

async function fetch_classify() {
  loading.value = true

  genres.value = []

  if (!track_id.value) {
    return
  }

  const result = await backend_instance.classify(track_id.value).catch(toast_error)

  loading.value = false

  if (!result) {
    return
  }

  console.log(result)

  for (const genre_id of result) {
    const genre = await backend_instance.get_genre(genre_id).catch(toast_error)

    if (!genre) {
      continue
    }

    genres.value.push(genre)
  }
}
</script>
