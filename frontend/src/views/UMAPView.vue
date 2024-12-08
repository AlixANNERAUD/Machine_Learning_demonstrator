<template>
  <div id="plot" class="h-dvh w-dvw">
    <Skeleton v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import HeroComponent from '@/components/HeroComponent.vue'
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { backend, toast_error } from '@/stores/backend'
import { height } from '@fortawesome/free-brands-svg-icons/fa42Group'
import Plotly from 'plotly.js-dist-min'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loading = ref(true)

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  loading.value = true

  console.log('fetching data')

  const response = await backend.get('/umap').catch(toast_error)

  console.log('label', response.data.labels)

  const trace = {
    x: response.data.x,
    y: response.data.y,
    z: response.data.z,
    text: response.data.labels,
    type: 'scatter3d',
    mode: 'markers',
    marker: {
      size: 3,
      color: response.data.z,
      colorscale: 'Viridis',
    },
  }

  const layout = {
    autosize: true,
    template: 'plotly_dark',
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: 0,
    },
  }

  Plotly.newPlot('plot', [trace], layout, { responsive: true })

  loading.value = false
}
</script>
