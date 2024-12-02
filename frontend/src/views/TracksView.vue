<template>
  <HeroComponent title="Tracks" subtitle="List of tracks">
    <!--Navigation bar-->
    <nav class="level">
      <div class="level-left">
        <!--Pagination-->
        <nav class="pagination" role="navigation" aria-label="pagination" v-if="total_pages > 1">
          <ul class="pagination-list">
            <li v-if="current_page > 2">
              <a class="pagination-link" aria-label="Goto page 1" @click="change_page(1)">1</a>
            </li>
            <li v-if="current_page > 2">
              <span class="pagination-ellipsis">&hellip;</span>
            </li>
            <li v-if="current_page > 1">
              <a
                class="pagination-link"
                aria-label="Goto page "
                @click="change_page(current_page - 1)"
                >{{ current_page - 1 }}</a
              >
            </li>

            <li>
              <a
                class="pagination-link is-current"
                aria-label="Page {{ page.number }}"
                aria-current="page"
                >{{ current_page }}</a
              >
            </li>

            <li v-if="current_page < total_pages">
              <a
                class="pagination-link"
                aria-label="Goto page "
                @click="change_page(current_page + 1)"
                >{{ current_page + 1 }}</a
              >
            </li>

            <li v-if="current_page < total_pages - 1">
              <span class="pagination-ellipsis">&hellip;</span>
            </li>
            <li v-if="current_page < total_pages">
              <a class="pagination-link" aria-label="Goto page" @click="change_page(total_pages)">{{
                total_pages
              }}</a>
            </li>
          </ul>
        </nav>
      </div>

      <!--Search bar-->
      <div class="level-item">
        <div class="field has-addons">
          <p class="control">
            <input class="input" type="text" placeholder="Find a track" v-model="search" />
          </p>
          <p class="control">
            <button class="button" @click="search_track">Search</button>
          </p>
        </div>
      </div>
    </nav>

    <!--Table-->
    <table class="table is-fullwidth">
      <thead>
        <tr>
          <th>
            <abbr title="Position">#</abbr>
          </th>
          <th>Date</th>
          <th>Name</th>
          <th>Artists</th>
          <th>Durations</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="track in tracks" :key="track.id">
          <td>{{ track.position }}</td>
          <td>{{ track.release_date }}</td>
          <td>{{ track.track_name }}</td>
          <td>
            <span v-for="(artist, index) in track.artists" :key="artist.artist_id">
              {{ artist.artist_name }}
              <span v-if="index < track.artists.length - 1">, </span>
            </span>
          </td>
          <td>{{ formatTime(track.track_duration_ms) }}</td>
        </tr>
      </tbody>
    </table>
  </HeroComponent>

  <ErrorModalComponent v-if="error" :message="error" @close="error = null" />
</template>

<script setup lang="ts">
import ErrorModalComponent from '@/components/ErrorModalComponent.vue'
import HeroComponent from '@/components/HeroComponent.vue'
import axiosInstance from '@/stores/axiosInstance'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const loading = ref(true)
const error = ref<string | null>(null)

interface Artist {
  artist_id: string
  artist_name: string
}

interface Track {
  id: number
  position: number
  release_date: string
  track_name: string
  artists: Artist[]
  track_duration_ms: number
}

const tracks = ref<Track[]>([])
const total_pages = ref<number>(0)
const route = useRoute()

const current_page = ref<number>(1)
const search = ref<string>('')

watch(() => route.params.id, fetch_data, { immediate: true })

function formatTime(ms: number) {
  const minutes = Math.floor(ms / 60000)
  const seconds = ((ms % 60000) / 1000).toFixed(0)
  return `${minutes}:${parseInt(seconds) < 10 ? '0' : ''}${seconds}`
}

async function fetch_data() {
  try {
    console.log('fetching data')

    const params: { page: number; search?: string } = {
      page: current_page.value,
    }

    if (search.value.length > 0) {
      params.search = search.value
    }

    const response = await axiosInstance.get('/tracks', { params })

    console.log('response', response.data)

    tracks.value = response.data.tracks.map((track: any) => {
      let artists: Artist[] = []

      try {
        artists = JSON.parse(track.artists.replace(/'/g, '"').replace(/`/g, '"'))
      } catch (e) {
        console.error(e)
      }

      return {
        ...track,
        artists,
      }
    })

    total_pages.value = response.data.total_pages

    console.log('data', tracks.value)
  } catch (e) {
    error.value = (e as Error).message
  } finally {
    loading.value = false
  }
}

function search_track() {
  current_page.value = 1
  fetch_data()
}

function change_page(page: number) {
  if (page < 1 || page > total_pages.value) {
    return
  }

  current_page.value = page
  fetch_data()
}
</script>
