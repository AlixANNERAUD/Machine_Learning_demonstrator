<script setup lang="ts">
import { Sidebar, SidebarContent, SidebarFooter, SidebarGroup, SidebarGroupContent, SidebarGroupLabel, SidebarHeader, SidebarMenu, SidebarMenuButton, SidebarMenuItem } from '@/components/ui/sidebar'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome';
import { fas } from '@fortawesome/free-solid-svg-icons';
import { useColorMode } from '@vueuse/core';
import Button from './ui/button/Button.vue';
import SidebarMenuSub from './ui/sidebar/SidebarMenuSub.vue';
import SidebarMenuSubItem from './ui/sidebar/SidebarMenuSubItem.vue';
import SidebarMenuSubButton from './ui/sidebar/SidebarMenuSubButton.vue';

const data_group = [
  { title: 'Tracks', icon: 'faMusic', url: '/tracks', },
  { title: 'Scrape', icon: 'faCloudArrowDown', url: '/scrape', },
  { title: 'UMAP', icon: 'faChartLine', url: '/umap' },
  { title: 'PCA', icon: 'faChartLine', url: '/pca' }
]

const composition_group = [
  { title: 'Search', icon: 'faSearch', url: '/search', },
  { title: 'Compose', icon: 'faWandMagicSparkles', url: '/compose', },
]

const groups = [
  { title: 'Data', icon: 'faDatabase', items: data_group },
  { title: 'Composition', icon: 'faMusic', items: composition_group },
]

const mode = useColorMode();

function toggle_mode() {
  mode.value = mode.value === 'dark' ? 'light' : 'dark';
}

</script>

<template>
  <Sidebar>
    <SidebarHeader>

    </SidebarHeader>

    <SidebarContent>
      <SidebarGroup>
        <SidebarMenu>
          <SidebarMenuItem v-for="group in groups" :key="group.title">
            <SidebarMenuButton>
              <FontAwesomeIcon :icon="fas[group.icon]" />
              {{ group.title }}
            </SidebarMenuButton>
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
    <SidebarFooter>
      <Button @click="toggle_mode" variant="outline" size="icon">
        <FontAwesomeIcon :icon="fas.faAdjust" />
      </Button>
    </SidebarFooter>

  </Sidebar>
</template>
