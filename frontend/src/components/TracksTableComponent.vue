<template>
  <div class="rounded-md border">
    <Table>
      <TableBody>
        <!--Table rows-->
        <TableRow v-for="track in tracks" :key="track.id">
          <!--Album cover-->
          <TableCell v-if="track.album">
            <img :src="track.album.cover_small" alt="album cover" />
          </TableCell>
          <!--Track title and artist-->
          <TableCell v-if="track.album">
            <strong>{{ track.title_short }}</strong><br />
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
            <router-link :to="{
              name: 'Compose',
              params: { track_id: track.id },
            }">
              <Button variant="outline">
                <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
              </Button>
            </router-link>
          </TableCell>
          <!--Play/Pause button-->
          <TableCell>
            <Button @click="play_pause">
              <audio controls class="hidden">
                <source :src="track.preview" type="audio/mpeg" />
              </audio>
              <FontAwesomeIcon :icon="fas.faPlay" />
            </Button>
          </TableCell>

        </TableRow>
      </TableBody>
    </Table>
  </div>
</template>

<script setup lang="ts">
const props = defineProps({
  tracks: Array,
});

import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import Button from './ui/button/Button.vue';
import Table from './ui/table/Table.vue';
import TableBody from './ui/table/TableBody.vue';
import TableCell from './ui/table/TableCell.vue';
import TableRow from './ui/table/TableRow.vue';
import { fas } from '@fortawesome/free-solid-svg-icons';
import format_time from '@/stores/utils';

interface Track {
  id: number;
  title_short: string;
  artist: {
    name: string;
  };
  album: {
    title: string;
    cover_small: string;
  };
  duration: number;
  artists: Array<{
    artist_id: number;
    artist_name: string;
  }>;
  preview: string;
}

function play_pause(event: MouseEvent) {
  const target = event.target as HTMLElement;

  const audio = target.querySelector('audio') as HTMLAudioElement;
  
  if (audio.paused) {
    audio.play()
  } else {
    audio.pause()
  }
}


</script>
