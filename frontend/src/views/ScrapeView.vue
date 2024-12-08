<template>
  <!--Columns-->
  <div class="columns-2 px-44 h-full">
    <!--First column : scraping-->
    <Card class="w-full">
      <CardHeader>
        <CardTitle>Scrape a playlist</CardTitle>
      </CardHeader>
      <CardContent>
        <div class="flex w-full max-w-sm items-center gap-1.5">
          <!--Input and button-->
          <Input
            class="input"
            type="text"
            placeholder="Playlist identifier"
            v-model="playlist_id"
            @input="fetch_playlist"
          />
          <!--Button-->
          <Button type="submit" @click="scrape">
            <FontAwesomeIcon :icon="fas.faCloudArrowDown" /> Scrape
          </Button>
        </div>

        <Card v-if="playlist || loading">
          <CardHeader>
            <CardTitle v-if="loading">
              <Skeleton class="w-1/2" />
            </CardTitle>

            <CardTitle v-if="playlist">{{ playlist.title }}</CardTitle>

            <CardDescription>{{ playlist.description }}</CardDescription>

            <CardDescription>
              <Skeleton class="w-1/2" v-if="loading" />
            </CardDescription>
          </CardHeader>
        </Card>
      </CardContent>
    </Card>

    <!--Second column : queue-->
    <div class="flex flex-col gap-4">
      <Card>
        <CardHeader>
          <CardTitle>Download queue</CardTitle>
        </CardHeader>
      </Card>
      <Card>
        <CardHeader>
          <CardTitle>Embedding queue</CardTitle>
        </CardHeader>
      </Card>
    </div>
  </div>
</template>

<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import Card from '@/components/ui/card/Card.vue'
import CardContent from '@/components/ui/card/CardContent.vue'
import CardDescription from '@/components/ui/card/CardDescription.vue'
import CardHeader from '@/components/ui/card/CardHeader.vue'
import CardTitle from '@/components/ui/card/CardTitle.vue'
import Input from '@/components/ui/input/Input.vue'
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { backend, toast_error } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { ref } from 'vue'

const playlist_id = ref('')
const loading = ref(false)
const playlist = ref(null)

async function fetch_playlist() {
  loading.value = true

  console.log(`Fetching playlist : ` + playlist_id.value)
  const result = await backend
    .get('/deezer/playlist', {
      params: {
        playlist_id: playlist_id.value,
      },
    })
    .catch(toast_error)

  playlist.value = result.data

  loading.value = false
}

const tracks = ref([])

async function scrape() {
  await backend.get('/deezer/scrape', {
    params: {
      playlist_id: playlist_id,
    },
  })
}
</script>
