<script setup lang="ts">
import { fas } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { ref } from 'vue'

defineProps<{
  message: string
}>()

const is_active = ref(true)

function close() {
  is_active.value = false
}
</script>

<template>
  <div class="modal" :class="{ 'is-active': is_active }">
    <div class="modal-background"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">
          <FontAwesomeIcon :icon="fas.faExclamationTriangle" />
          Something went wrong ...
        </p>
        <button class="delete" aria-label="close" @click="close"></button>
      </header>
      <section class="modal-card-body" id="error-modal-content">
        {{ message }}
      </section>
    </div>
  </div>
</template>
