<template>
  <div class="lg:px-24 py-6">
    <!--Navigation bar-->
    <div class="flex gap-2 items-center py-4">
      <!--Search bar-->
      <div class="relative w-full max-w-sm items-center">
        <Input class="pl-10" placeholder="Filter tracks ..." @input="search_track" />

        <span class="absolute start-0 inset-y-0 flex items-center justify-center px-4">
          <FontAwesomeIcon :icon="fas.faSearch" />
        </span>
      </div>

      <!--Pagination-->
      <Pagination class="ml-auto">
        <PaginationList class="flex">
          <Button
            v-if="current_page > 2"
            class="w-10 h-10 p-0"
            variant="outline"
            @click="change_page(1)"
            >1</Button
          >
          <PaginationEllipsis v-if="current_page > 2" />
          <Button
            v-if="current_page > 1"
            class="w-10 h-10 p-0"
            variant="outline"
            @click="change_page(current_page - 1)"
          >
            {{ current_page - 1 }}
          </Button>
          <Button class="w-10 h-10 p-0" variant="default" @click="change_page(current_page)">
            {{ current_page }}
          </Button>
          <Button
            v-if="current_page < total_pages"
            class="w-10 h-10 p-0"
            variant="outline"
            @click="change_page(current_page + 1)"
          >
            {{ current_page + 1 }}
          </Button>
          <PaginationEllipsis v-if="current_page < total_pages - 1" />
          <Button
            v-if="current_page < total_pages - 1"
            class="w-10 h-10 p-0"
            variant="outline"
            @click="change_page(total_pages)"
          >
            {{ total_pages }}
          </Button>
        </PaginationList>
      </Pagination>
    </div>

    <!--Table-->
    <Skeleton v-if="loading" />
    <MusicTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import MusicTableComponent from '@/components/TracksTableComponent.vue'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import { Pagination, PaginationList } from '@/components/ui/pagination'
import PaginationEllipsis from '@/components/ui/pagination/PaginationEllipsis.vue'
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { backend, toast_error, type Track } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { toast } from 'vue-sonner'

const loading = ref(true)

const route = useRoute()

const tracks = ref<Track[]>([])
const total_pages = ref<number>(0)
const current_page = ref<number>(1)
let search = ''

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  loading.value = true

  const params: { page: number; search?: string } = {
    page: current_page.value,
  }

  if (search.length > 0) {
    params.search = search
  }

  const response = await backend.get('/tracks', { params }).catch(toast_error)

  loading.value = false

  if (!response) {
    toast.error('No response from server')
    return
  }

  tracks.value = response.data.tracks

  total_pages.value = response.data.total_pages
}

function search_track(event: InputEvent) {
  const target = event.target as HTMLInputElement
  search = target.value

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
