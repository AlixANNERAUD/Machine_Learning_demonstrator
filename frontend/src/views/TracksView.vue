<template>
  <div class="px-44">
    <!--Navigation bar-->
    <div class="flex gap-2 items-center py-4">
      <!--Search bar-->
      <Input class="max-w-sm" placeholder="Filter tracks ..." v-model="search" @input="search_track" />
      <!--Pagination-->
      <Pagination class="ml-auto">
        <PaginationList>
          <Button v-if="current_page > 2" class="w-10 h-10 p-0" variant="outline" @click="change_page(1)">1</Button>
          <PaginationEllipsis v-if="current_page > 2" />
          <Button v-if="current_page > 1" class="w-10 h-10 p-0" variant="outline"
            @click="change_page(current_page - 1)"> {{ current_page - 1 }} </Button>
          <Button class="w-10 h-10 p-0" variant="default" @click="change_page(current_page)"> {{ current_page }}
          </Button>
          <Button v-if="current_page < total_pages" class="w-10 h-10 p-0" variant="outline"
            @click="change_page(current_page + 1)">
            {{ current_page + 1 }}
          </Button>
          <PaginationEllipsis v-if="current_page < total_pages - 1" />
          <Button v-if="current_page < total_pages - 1" class="w-10 h-10 p-0" variant="outline"
            @click="change_page(total_pages)">
            {{ total_pages }}
          </Button>

        </PaginationList>
      </Pagination>
    </div>

    <!--Table-->
    <MusicTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import MusicTableComponent from '@/components/TracksTableComponent.vue'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import { Pagination, PaginationList } from '@/components/ui/pagination'
import PaginationEllipsis from '@/components/ui/pagination/PaginationEllipsis.vue'
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

const route = useRoute()

const tracks = ref<Track[]>([])
const total_pages = ref<number>(0)
const current_page = ref<number>(1)
const search = ref<string>('')

watch(() => route.params.id, fetch_data, { immediate: true })

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

    tracks.value = response.data.tracks.map(parse_tracks)

    total_pages.value = response.data.total_pages

  } catch (e) {
    error.value = (e as Error).message
  } finally {
    loading.value = false
  }
}

function parse_tracks(track): Artist[] {
  try {
    const artists = JSON.parse(track.artists.replace(/'/g, '"').replace(/`/g, '"'))

    return {
      ...track,
      artists,
    }
  } catch {
    console.warn('Failed to parse artists for track', track)
    return {
      ...track,
      artists: [],
    }
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
