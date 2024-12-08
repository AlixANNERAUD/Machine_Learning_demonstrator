<template>
  <!--Columns-->
  <div class="columns-2 px-44">
    <!--First column : scraping-->
    <h2>Scrape a playlist</h2>
    <div>
      <!--Input and button-->
      <Input class="input" type="text" placeholder="Playlist identifier" v-model="playlist_id"
        @input="fetch_playlist" />
      <!--Button-->
      <Button @click="scrape">
        <FontAwesomeIcon :icon="fas.faCloudArrowDown" /> Scrape
      </Button>

      <Card v-if="playlist">
        <CardHeader>
          <CardTitle>{{ playlist.title }}</CardTitle>
          <CardTitle>{{ playlist.description }}</CardTitle>
        </CardHeader>
      </Card>


    </div>
    <!--Second column : queue-->
    <div>
      <h2>Queue</h2>

    </div>
  </div>
</template>

<script setup lang="ts">
import Card from '@/components/ui/card/Card.vue';
import CardHeader from '@/components/ui/card/CardHeader.vue';
import CardTitle from '@/components/ui/card/CardTitle.vue';
import Input from '@/components/ui/input/Input.vue';
import axiosInstance from '@/stores/axiosInstance';
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { ref } from 'vue'

const playlist_id = ref('')

const playlist = ref(null)

async function fetch_playlist() {
  const result = await axiosInstance.get('/deezer/playlist', {
    params: {
      playlist_id: playlist_id.value,
    },
  })

  playlist.value = result.data
}

const tracks = ref([])

async function scrape() {
  await axiosInstance.get('/deezer/scrape', {
    params: {
      playlist_id: playlist_id,
    },
  })
}
</script>
