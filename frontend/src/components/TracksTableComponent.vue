<template>
  <div class="rounded-md border">
    <Table>
      <TableBody>
        <!--Table rows-->
        <TableRow v-for="track in tracks" :key="track.id">
          <!--Album cover-->
          <TableCell v-if="track.album">
            <img :src="track.album.cover_small" class="min-w-6" alt="album cover" />
          </TableCell>
          <!--Track title and artist-->
          <TableCell v-if="track.album">
            <strong>{{ track.title_short }}</strong
            ><br />
            {{ track.artist.name }}
          </TableCell>
          <!--Album title-->
          <TableCell v-if="track.album"> {{ track.album.title }} </TableCell>
          <!--Duration-->
          <TableCell> {{ format_time(track.duration) }} </TableCell>
          <TableCell>
            <span v-for="(artist, index) in track.artists" :key="artist.artist_id">
              {{ artist.artist_name }}
              <span v-if="index < track.artists.length - 1">, </span>
            </span>
          </TableCell>
          <!--Compose button-->
          <TableCell>
            <router-link
              :to="{
                name: 'Compose',
                params: { track_id: track.id },
              }"
            >
              <Button variant="outline">
                <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
              </Button>
            </router-link>
          </TableCell>
          <!--Classify button-->
          <TableCell>
            <router-link
              :to="{
                name: 'Classify',
                params: { track_id: track.id },
              }"
            >
              <Button variant="outline">
                <FontAwesomeIcon :icon="fas.faLayerGroup" />
              </Button>
            </router-link>
          </TableCell>
          <!--Play/Pause button-->
          <TableCell>
            <Button @click="play_pause" :data-track-id="track.id">
              <audio controls class="hidden">
                <source :src="track.preview" type="audio/mpeg" />
              </audio>
              <FontAwesomeIcon
                class="status-playing block"
                :icon="!!track.playing ? fas.faPause : fas.faPlay"
              />
            </Button>
          </TableCell>
        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  tracks: Array<Track>,
})

const tracks = ref(props.tracks)

import { format_time } from '@/stores/utils'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue'
import Button from './ui/button/Button.vue'
import Table from './ui/table/Table.vue'
import TableBody from './ui/table/TableBody.vue'
import TableCell from './ui/table/TableCell.vue'
import TableRow from './ui/table/TableRow.vue'
import type { Track } from '@/stores/backend'

function play_pause(event: MouseEvent) {
  const target = event.target as HTMLElement

  const audio = target.querySelector('audio') as HTMLAudioElement

  if (audio.paused) {
    audio.play()
  } else {
    audio.pause()
  }

  audio.onended = () => {
    audio.currentTime = 0
    audio.pause()
    tracks.value = tracks.value?.map((track: Track) => {
      track.playing = false
      return track
    })
  }

  const track_id = target.dataset.trackId
  // update tracks
  tracks.value = tracks.value?.map((track: Track) => {
    if (track.id === Number(track_id)) {
      track.playing = !track.playing
    }
    return track
  })
}
</script>
