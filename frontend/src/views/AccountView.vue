<template>
  <main>
    <HeroComponent title="Account" subtitle="Check the details of your account.">
      <p class="is-size-4">
        👋 Hello, {{ profile?.display_name }} (aka
        <a :href="profile?.external_urls.spotify" target="_blank">{{ profile?.id }} !</a>)
      </p>
      <p></p>

      <nav class="level">
        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Playlists</p>
            <p v-if="loading" class="title is-skeleton">Loading...</p>
            <p v-if="profile" class="title">{{ playlists?.items.length }}</p>
          </div>
        </div>

        <div class="level-item has-text-centered">
          <div>
            <p class="heading">Followers</p>
            <p v-if="loading" class="title is-skeleton">Loading...</p>
            <p v-if="profile" class="title">{{ profile?.followers.total }}</p>
          </div>
        </div>
        <div class="level-item has-text-centered">
          <button class="button is-primary" @click="logout">Logout</button>
        </div>
      </nav>

      <div class="grid is-col-min-15">
        <div v-for="playlist in playlists?.items" :key="playlist?.id" class="cell card">
          <div class="card-content">
            <div class="media">
              <div v-if="playlist?.images" class="media-left">
                <figure class="image is-48x48">
                  <img :src="playlist?.images[0].url" alt="Playlist image" />
                </figure>
              </div>
              <div class="media-content">
                <p class="title is-4">
                  <a href="#">{{ playlist?.name }}</a>
                </p>
                <p class="subtitle is-6">
                  {{ playlist?.tracks?.total }} tracks -
                  {{ playlist?.public ? 'Public' : 'Private' }}
                </p>
              </div>
            </div>
            <div class="content">{{ playlist?.description }}</div>
            <br />
          </div>
        </div>
      </div>
    </HeroComponent>

    <ErrorModalComponent v-if="error" :message="error" @close="error = null" />
  </main>
</template>

<script setup lang="ts">
import HeroComponent from '../components/HeroComponent.vue'
import ErrorModalComponent from '../components/ErrorModalComponent.vue'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const profile = ref<null>(null)
const loading = ref(true)
const playlists = ref<null>(null)
const error = ref<string | null>(null)

watch(() => route.params.id, fetch_data, { immediate: true })
async function fetch_data() {

}

function logout() {
  localStorage.clear()
  sessionStorage.clear()
  window.location.href = '/'
}
</script>
