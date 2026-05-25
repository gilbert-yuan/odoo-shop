<template>
  <StaticPage
    title="COA Lookup"
    description="Find the Certificate of Analysis for any NextPept batch."
  >
    <p class="muted">
      Enter the lot number printed on your vial (e.g. <code>NPB-2026-0042</code>) to retrieve
      the Certificate of Analysis (HPLC + mass spectrometry).
    </p>

    <form class="search" @submit.prevent="lookup">
      <input
        v-model="code"
        class="input"
        type="search"
        placeholder="Lot number or batch code"
        required
      />
      <button class="button primary" type="submit" :disabled="loading">
        {{ loading ? "Searching…" : "Find COA" }}
      </button>
    </form>

    <div v-if="error" class="card msg error">{{ error }}</div>

    <section v-if="searched && !loading">
      <div v-if="!items.length" class="card msg muted">
        No documents matched <strong>{{ lastCode }}</strong>. Double-check the lot number
        from the vial label, or
        <RouterLink to="/contact">contact support</RouterLink>.
      </div>
      <div v-else class="results">
        <article v-for="item in items" :key="item.id" class="card row">
          <div>
            <strong>{{ item.name }}</strong>
            <p v-if="item.mimetype" class="muted small">{{ item.mimetype }}</p>
          </div>
          <a :href="item.url" class="button primary" download>Download</a>
        </article>
      </div>
    </section>
  </StaticPage>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";

import StaticPage from "./StaticPage.vue";
import { odooApi } from "../services/odooApi";

const code = ref("");
const lastCode = ref("");
const items = ref([]);
const loading = ref(false);
const error = ref("");
const searched = ref(false);

async function lookup() {
  const value = code.value.trim();
  if (!value) return;
  loading.value = true;
  error.value = "";
  try {
    items.value = await odooApi.lookupCoa(value);
    lastCode.value = value;
    searched.value = true;
  } catch (e) {
    error.value = e.message || "Lookup failed.";
  } finally {
    loading.value = false;
  }
}
</script>

<style scoped>
.search {
  display: grid;
  grid-template-columns: 1fr auto;
  gap: 0.6rem;
  margin: 0.8rem 0 0.4rem;
}

code {
  font-family: ui-monospace, monospace;
  background: rgba(13, 128, 102, 0.08);
  padding: 0.05rem 0.4rem;
  border-radius: 4px;
}

.msg {
  padding: 1rem;
  margin-top: 1rem;
  text-align: center;
}

.msg.error {
  color: var(--danger);
  border-color: var(--danger);
}

.results {
  display: grid;
  gap: 0.5rem;
  margin-top: 1rem;
}

.row {
  padding: 0.85rem 1rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1rem;
}

.row p {
  margin: 0.2rem 0 0;
}

.small {
  font-size: 0.8rem;
}

@media (max-width: 540px) {
  .search {
    grid-template-columns: 1fr;
  }
  .row {
    flex-direction: column;
    align-items: stretch;
    text-align: center;
  }
}
</style>
