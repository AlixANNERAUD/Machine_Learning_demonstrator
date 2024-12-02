<template>
  <HeroComponent title="Compose" subtitle="Find matches">
    <div class="field has-addons">
      <p class="control">
        <input class="input" type="text" placeholder="Find a track" v-model="track" />
      </p>
      <p class="control">
        <button class="button" @click="compose">
          <FontAwesomeIcon :icon="fas.faWandMagicSparkles" /> Compose
        </button>
      </p>
    </div>
  </HeroComponent>
</template>

<script setup lang="ts">
import { defineProps, ref, toRefs } from 'vue'
import HeroComponent from '@/components/HeroComponent.vue'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import axiosInstance from '@/stores/axiosInstance'

const props = defineProps({
  track: String,
})

const { track } = toRefs(props)

const tracks = ref([])

console.log('ComposeView : ', track?.value)

async function fetch_data() {
  const result = axiosInstance.get('/compose', {
    params: {
      track: track?.value,
    },
  })

  tracks.value = (await result).data
}

function compose() {
  console.log('ComposeView : compose')
  fetch_data()
}
</script>
