<template>
  <div class="flex justify-center items-center h-screen">
    <Card class="w-1/2">
      <CardHeader>
        <CardTitle> Deez'Nalyzer </CardTitle>
        <CardDescription> Analyze and compose music from Deezer's API </CardDescription>
      </CardHeader>

      <CardContent>
        This is a simple web application that allows you to search for tracks on

        <a href="https://www.deezer.com/">Deezer API</a>, analyze them, and compose new tracks based
        on the analysis.
        <p>The application is built with Vue 3, Tailwind CSS, and Vite.</p>
      </CardContent>
    </Card>
  </div>
</template>

<script setup lang="ts">
import Card from '@/components/ui/card/Card.vue'
import CardContent from '@/components/ui/card/CardContent.vue'
import CardDescription from '@/components/ui/card/CardDescription.vue'
import CardHeader from '@/components/ui/card/CardHeader.vue'
import CardTitle from '@/components/ui/card/CardTitle.vue'
</script>
