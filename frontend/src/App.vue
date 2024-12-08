<template>
  <SidebarProvider>
    <MainSidebar />
    <main>
      <SidebarTrigger />

      <RouterView />
    </main>
  </SidebarProvider>

</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import SidebarProvider from './components/ui/sidebar/SidebarProvider.vue';
import MainSidebar from './components/MainSidebar.vue';
import SidebarTrigger from './components/ui/sidebar/SidebarTrigger.vue';
</script>
