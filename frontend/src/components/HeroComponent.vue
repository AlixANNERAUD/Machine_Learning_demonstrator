<script setup lang="ts">
defineProps<{
  title: string
  subtitle: string
}>()
</script>

<template>
  <div class="hero is-fullheight">
    <div class="hero-head has-text-centered">
      <section class="section is-small">
        <p class="title" id="main-title">
          {{ title }}
        </p>
        <p class="subtitle" id="main-subtitle">
          {{ subtitle }}
        </p>
      </section>
    </div>
    <div class="hero-body">
      <div class="container" id="main-content">
        <div class="content">
          <slot/>
        </div>
      </div>
    </div>

    <div class="hero-foot">
      <div class="section has-text-centered is-small">
        <p>
          <a href="https://alix.anneraud.fr">Alix ANNERAUD</a>
          - Josselin DULONGCOURTY - Mathis SAUNIER
        </p>
      </div>
    </div>
  </div>
</template>
