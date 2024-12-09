<template>
  <SidebarProvider>
    <MainSidebar />
    <main class="relative w-full h-screen">
      <RouterView />

      <SidebarTrigger class="absolute top-0 left-0" />
    </main>
  </SidebarProvider>

  <Toaster />
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { Toaster } from 'vue-sonner'
import MainSidebar from './components/MainSidebar.vue'
import SidebarProvider from './components/ui/sidebar/SidebarProvider.vue'
import SidebarTrigger from './components/ui/sidebar/SidebarTrigger.vue'
</script>
