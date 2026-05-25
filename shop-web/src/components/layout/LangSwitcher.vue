<template>
  <div class="lang">
    <button
      v-for="locale in locales"
      :key="locale.code"
      type="button"
      class="opt"
      :class="{ active: current === locale.code }"
      @click="change(locale.code)"
    >
      {{ locale.label }}
    </button>
  </div>
</template>

<script setup>
import { computed } from "vue";

import { i18n, setLocale, SUPPORTED_LOCALES } from "../../i18n";

const locales = SUPPORTED_LOCALES;
const current = computed(() => i18n.global.locale.value);

function change(code) {
  setLocale(code);
}
</script>

<style scoped>
.lang {
  display: inline-flex;
  border: 1px solid var(--line);
  border-radius: 999px;
  overflow: hidden;
  background: #fff;
}

.opt {
  border: 0;
  background: transparent;
  padding: 0.32rem 0.7rem;
  cursor: pointer;
  font: inherit;
  font-size: 0.85rem;
  color: var(--muted);
}

.opt:hover {
  color: var(--ink);
}

.opt.active {
  background: var(--accent);
  color: white;
  font-weight: 600;
}
</style>
