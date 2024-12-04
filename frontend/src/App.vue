<template>
  <div class="columns">
    <div class="column is-narrow">
      <section class="section is-small">
        <aside class="menu">
          <p class="menu-label">
            <i class="fa-solid fa-home"></i>
            <FontAwesomeIcon :icon="fas.faHome" />
            General
          </p>
          <ul class="menu-list">
            <li>
              <router-link to="/" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faTachometerAlt" /> Dashboard</a
                >
              </router-link>
            </li>
          </ul>
          <p class="menu-label">
            <i class="fa-solid fa-user"></i>
            <FontAwesomeIcon :icon="fas.faUser" />
            Account
          </p>
          <ul class="menu-list">
            <li>
              <router-link to="/account" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faUser" />
                  Details</a
                >
              </router-link>
            </li>
          </ul>
          <p class="menu-label">
            <FontAwesomeIcon :icon="fas.faDatabase" />
            Data
          </p>
          <ul class="menu-list">
            <li>
              <router-link to="/tracks" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faMusic" />
                  Tracks</a
                >
              </router-link>
            </li>
            <li>
              <router-link to="/scrape" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faCloudArrowDown" />
                  Scrape</a
                >
              </router-link>
            </li>
            <li>
              <router-link to="/umap" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faChartLine" />
                  UMAP</a
                >
              </router-link>
            </li>
            <li>
              <router-link to="/pca" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faChartLine" />
                  PCA</a
                >
              </router-link>
            </li>
          </ul>
          <p class="menu-label">
            <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
            Composition
          </p>
          <ul class="menu-list">
            <li>
              <router-link to="/search" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faSearch" />
                  Search</a
                >
              </router-link>
            </li>
            <li>
              <router-link to="/compose" custom v-slot="{ href, navigate, isActive }">
                <a :class="{ 'is-active': isActive }" :href="href" @click="navigate">
                  <FontAwesomeIcon :icon="fas.faWandMagicSparkles" />
                  Compose</a
                >
              </router-link>
            </li>
          </ul>
        </aside>
      </section>
    </div>

    <div class="column">
      <div id="main-content">
        <RouterView />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { RouterView } from 'vue-router'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { fas } from '@fortawesome/free-solid-svg-icons'
</script>
