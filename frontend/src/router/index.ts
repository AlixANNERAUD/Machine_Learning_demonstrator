import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import TracksView from '@/views/TracksView.vue'
import UMAPView from '@/views/UMAPView.vue'
import PCAView from '@/views/PCAView.vue'
import SearchView from '@/views/SearchView.vue'
import ComposeView from '@/views/ComposeView.vue'
import ScrapeView from '@/views/ScrapeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: DashboardView,
    },
    {
      path: '/tracks',
      name: 'Tracks',
      component: TracksView,
    },
    {
      path: '/umap',
      name: 'UMAP',
      component: UMAPView,
    },
    {
      path: '/pca',
      name: 'PCA',
      component: PCAView,
    },
    {
      path: '/compose/:track_id?/:preview_url?',
      name: 'Compose',
      component: ComposeView,
      props: true,
    },
    {
      path: '/search',
      name: 'Search',
      component: SearchView,
    },
    {
      path: '/scrape',
      name: 'Scrape',
      component: ScrapeView,
    },
  ],
})

export default router
