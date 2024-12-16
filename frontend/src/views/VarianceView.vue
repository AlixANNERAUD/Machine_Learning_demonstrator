<template>
  <div id="plot" class="w-full h-screen">
    <Skeleton v-if="loading" />
  </div>
</template>

<script setup lang="ts">
import Skeleton from '@/components/ui/skeleton/Skeleton.vue'
import { backend_instance, toast_error } from '@/stores/backend'
import { cumulative_sum } from '@/stores/utils'
import { newPlot, type Layout, type PlotData } from 'plotly.js-dist-min'
import { ref, watch } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const loading = ref(true)

watch(() => route.params.id, fetch_data, { immediate: true })

async function fetch_data() {
  loading.value = true

  const response = await backend_instance.get_explained_variance_ratio().catch(toast_error)

  if (!response) {
    return
  }

  const cumsum = cumulative_sum(response)

  const trace: Partial<PlotData> = {
    x: ['x', 'y', 'z'],
    y: cumsum,
    type: 'bar',
  }

  const layout: Partial<Layout> = {
    title: {
      text: 'Explained variance ratio',
    },
    xaxis: {
      title: {
        text: 'Principal component',
      },
    },
    yaxis: {
      title: {
        text: 'Cumulative explained variance',
      },
    },
  }

  newPlot('plot', [trace], layout, { responsive: true })

  loading.value = false
}
</script>
