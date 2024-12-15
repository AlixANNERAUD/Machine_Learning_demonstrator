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
    <TracksTableComponent v-if="tracks.length" :tracks="tracks" />
  </div>
</template>

<script setup lang="ts">
import TracksTableComponent from '@/components/TracksTableComponent.vue'
import Button from '@/components/ui/button/Button.vue'
import Input from '@/components/ui/input/Input.vue'
import { Pagination, PaginationList } from '@/components/ui/pagination'
import PaginationEllipsis from '@/components/ui/pagination/PaginationEllipsis.vue'
import { backend_instance, toast_error, type Track } from '@/stores/backend'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const loading = ref(true)

const route = useRoute()

const tracks = ref<Array<Track>>([])
const total_pages = ref<number>(0)
const current_page = ref<number>(1)
let search = ''

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  loading.value = true

  const response = await backend_instance.get_tracks(current_page.value, search).catch(toast_error)

  console.log('response', response)

  loading.value = false

  if (!response) {
    return
  }

  console.log('tracks', tracks.value)

  console.log('response  2', response)

  tracks.value = response[0]
  total_pages.value = response[1]

  console.log('tracks', tracks.value)

  console.log('total_pages', total_pages.value)
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
