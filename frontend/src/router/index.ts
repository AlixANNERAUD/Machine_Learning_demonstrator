import { createRouter, createWebHistory } from 'vue-router'
import DashboardView from '@/views/DashboardView.vue'
import AccountView from '@/views/AccountView.vue'
import TracksView from '@/views/TracksView.vue'
import UMAPView from '@/views/UMAPView.vue'
import PCAView from '@/views/PCAView.vue'
import SearchView from '@/views/SearchView.vue'
import ComposeView from '@/views/ComposeView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: DashboardView,
    },
    {
      path: '/account',
      name: 'Account',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: AccountView,
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
      path: '/compose/:track?',
      name: 'Compose',
      component: ComposeView,
      props: true,
    },
    {
      path: '/search',
      name: 'Search',
      component: SearchView,
    },
  ],
})

export default router
