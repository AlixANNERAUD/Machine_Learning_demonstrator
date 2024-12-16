<script setup lang="ts">
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuSub,
  SidebarMenuSubItem,
  SidebarMenuSubButton,
  SidebarMenuItem,
} from '@/components/ui/sidebar'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
import { useColorMode } from '@vueuse/core'
import Button from './ui/button/Button.vue'
import { fab } from '@fortawesome/free-brands-svg-icons'
import { Separator } from './ui/separator'

const data_group = [
  { title: 'Tracks', icon: 'faMusic', url: '/tracks' },
  { title: 'Scrape', icon: 'faCloudArrowDown', url: '/scrape' },
  { title: 'UMAP', icon: 'faChartLine', url: '/umap' },
  { title: 'PCA', icon: 'faChartLine', url: '/pca' },
  { title: 'Variance', icon: 'faScaleUnbalanced', url: '/variance' },
]

const composition_group = [
  { title: 'Search', icon: 'faSearch', url: '/search' },
  { title: 'Compose', icon: 'faWandMagicSparkles', url: '/compose' },
  { title: 'Classify', icon: 'faLayerGroup', url: '/classify' },
]

const groups = [
  { title: 'Data', icon: 'faDatabase', items: data_group },
  { title: 'Composition', icon: 'faMusic', items: composition_group },
]

const mode = useColorMode()

function toggle_mode() {
  mode.value = mode.value === 'dark' ? 'light' : 'dark'
}
</script>

<template>
  <Sidebar>
    <!-- Header -->
    <SidebarHeader>
      <div class="p-4">
        <h3 class="text-2xl font-semibold leading-none tracking-tight text-center">
          <a href="/">Deez'Nalyzer</a>
        </h3>
        <p class="text-sm text-muted-foreground text-center">
          Analyze and compose music from Deezer's API
        </p>
      </div>
      <Separator />
    </SidebarHeader>
    <!-- Content -->
    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="group in groups" :key="group.title">
            <!--Menu title-->
            <SidebarMenuButton>
              <FontAwesomeIcon :icon="fas[group.icon]" />
              {{ group.title }}
            </SidebarMenuButton>
            <!-- Submenu -->
            <SidebarMenuSub>
              <SidebarMenuSubItem v-for="item in group.items" :key="item.title">
                <router-link :to="item.url" v-slot="{ isActive }">
                  <SidebarMenuSubButton asChild :isActive="isActive">
                    <span>
                      <FontAwesomeIcon :icon="fas[item.icon]" />
                      {{ item.title }}
                    </span>
                  </SidebarMenuSubButton>
                </router-link>
              </SidebarMenuSubItem>
            </SidebarMenuSub>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarGroup>
    </SidebarContent>
    <!-- Footer -->
    <SidebarFooter>
      <!--Buttons-->
      <div class="flex justify-center items-center gap-4">
        <!--Color mode-->
        <Button @click="toggle_mode" variant="outline" size="icon">
          <FontAwesomeIcon :icon="fas.faAdjust" />
        </Button>
        <!--GitHub-->
        <Button variant="outline" size="icon" as-child>
          <a href="https://github.com/AlixANNERAUD/Machine_learning_demonstrator">
            <FontAwesomeIcon :icon="fab.faGithub" />
          </a>
        </Button>
      </div>

      <Separator />
      <!--Credits-->
      <div class="px-4 py-2 text-sm text-muted-foreground">
        <p>Made with ❤️ by :</p>
        <ul class="list-disc list-inside">
          <li><a class="underline" href="https://alix.anneraud.fr">Alix ANNERAUD</a></li>
          <li><a class="underline" href="https://josselinonduty.fr">Josselin DULONGCOURTY</a></li>
          <li><a class="underline" href="https://mathis-saunier.fr">Mathis SAUNIER</a></li>
        </ul>
      </div>
    </SidebarFooter>
  </Sidebar>
</template>
