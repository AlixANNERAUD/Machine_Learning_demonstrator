import { createRouter, createWebHistory } from 'vue-router'
const DashboardView = () => import('@/views/DashboardView.vue')
const TracksView = () => import('@/views/TracksView.vue')
const UMAPView = () => import('@/views/UMAPView.vue')
const PCAView = () => import('@/views/PCAView.vue')
const SearchView = () => import('@/views/SearchView.vue')
const ComposeView = () => import('@/views/ComposeView.vue')
const ScrapeView = () => import('@/views/ScrapeView.vue')
const ClassifyView = () => import('@/views/ClassifyView.vue')

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
    {
      path: '/classify/:track_id?/:preview_url?',
      name: 'Classify',
      component: ClassifyView,
      props: true,
    },
  ],
})

export default router
