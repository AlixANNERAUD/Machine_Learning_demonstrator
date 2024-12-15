<template>
  <!--Columns-->
  <div class="flex flex-row items-start lg:px-44 gap-4 py-6">
    <!--First column : scraping-->
    <Card class="w-1/3">
      <div>
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

          <!--Playlist card-->
          <Card v-if="playlist || loading" class="mt-4">
            <CardHeader>
              <CardTitle v-if="loading">
                <Skeleton class="h-6 w-33" />
              </CardTitle>

              <img
                v-if="playlist"
                :src="playlist.picture_medium"
                alt="playlist cover"
                class="w-40 h-40 rounded-lg"
              />

              <CardTitle v-if="playlist">{{ playlist.title }}</CardTitle>

              <CardDescription v-if="playlist">{{ playlist.description }}</CardDescription>

              <CardDescription>
                <Skeleton class="h-6 w-40" v-if="loading" />
              </CardDescription>
            </CardHeader>
          </Card>
        </CardContent>
      </div>
    </Card>
    <!--Second column : queue-->
    <Card class="w-1/3">
      <div>
        <CardHeader>
          <CardTitle>
            <FontAwesomeIcon :icon="fas.faCloudArrowDown" />
            Download queue
            <span v-if="download_queue.length > 0"> ({{ download_queue.length }}) </span>
          </CardTitle>
          <Table>
            <TableBody>
              <TableRow v-for="track_id in download_queue" :key="track_id">
                <TableCell>
                  {{ track_id }}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardHeader>
      </div>
    </Card>

    <Card class="w-1/3">
      <div>
        <CardHeader>
          <CardTitle>
            <FontAwesomeIcon :icon="fas.faCloudArrowDown" />
            Embedding queue
            <span v-if="embedding_queue.length > 0"> ({{ embedding_queue.length }}) </span>
          </CardTitle>
          <Table>
            <TableBody>
              <TableRow v-for="track_id in embedding_queue" :key="track_id">
                <TableCell>
                  {{ track_id }}
                </TableCell>
              </TableRow>
            </TableBody>
          </Table>
        </CardHeader>
      </div>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Button from '@/components/ui/button/Button.vue'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import Input from '@/components/ui/input/Input.vue'
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { Table, TableBody, TableCell, TableRow } from '@/components/ui/table'
import { backend_instance, type Playlist, toast_error } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

import { onMounted, onUnmounted, ref } from 'vue'
import { toast } from 'vue-sonner'

let interval: ReturnType<typeof setTimeout> | null = null

onMounted(() => {
  interval = setInterval(fetch_queues, 2000)
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

const playlist_id = defineModel<string>('')

const loading = ref(false)
const playlist = ref<Playlist | null>(null)

const download_queue = ref<string[]>([])
const embedding_queue = ref<string[]>([])

async function fetch_queues() {
  const result = await backend_instance.get_queues().catch(toast_error)

  if (!result) {
    return
  }

  download_queue.value = result[0]
  embedding_queue.value = result[1]
}

async function fetch_playlist(event: InputEvent) {
  loading.value = true

  playlist.value = null

  if (!event.target) {
    toast.error('No target in event')
    return
  }

  const target = event.target as HTMLInputElement
  const playlist_id = target.value

  if (!playlist_id) {
    return
  }

  const result = await backend_instance.get_playlist(playlist_id).catch(toast_error)

  loading.value = false

  if (!result) {
    return
  }

  playlist.value = result
}

async function scrape() {
  if (!playlist_id.value) {
    toast.error('No playlist id')
    return
  }

  await backend_instance.scrape(playlist_id.value).catch(toast_error)

  toast.success('Scraping started')
}
</script>
