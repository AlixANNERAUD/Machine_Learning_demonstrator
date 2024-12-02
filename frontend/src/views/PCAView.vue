<template>
  <HeroComponent title="PCA" subtitle="PCA visualization">
    <div id="plot" class="plot-container"></div>
  </HeroComponent>
</template>

<style>
.plot-container {
  width: 100%;
  height: 65vh;
}
</style>

<script setup lang="ts">
import HeroComponent from '@/components/HeroComponent.vue'
import axiosInstance from '@/stores/axiosInstance'
import { height } from '@fortawesome/free-brands-svg-icons/fa42Group'
import Plotly from 'plotly.js-dist-min'
import { text } from 'stream/consumers'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loading = ref(true)
const error = ref<string | null>(null)
const data = ref<string | null>(null)

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  try {
    console.log('fetching data')

    const response = await axiosInstance.get('/pca')

    console.log("label", response.data.labels)

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
  } catch (err) {
    error.value = (err as Error).toString()
  } finally {
    loading.value = false
  }
}
</script>
