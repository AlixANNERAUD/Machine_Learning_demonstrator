<template>
  <div id="plot" class="w-full h-screen">
    <Skeleton v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { backend, toast_error } from '@/stores/backend'
import { newPlot, type Layout, type PlotData } from 'plotly.js-dist-min'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loading = ref(true)

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  loading.value = true

  const response = await backend.get('/pca').catch(toast_error)

  if (!response) {
    return
  }

  const trace: Partial<PlotData> = {
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

  const layout: Partial<Layout> = {
    autosize: true,
    margin: {
      l: 0,
      r: 0,
      b: 0,
      t: 0,
    },
  }

  newPlot('plot', [trace], layout, { responsive: true })

  loading.value = false
}
</script>
