<template>
  <section class="card picker">
    <header class="head">
      <h3>{{ title }}</h3>
      <button v-if="!showForm" class="button ghost" type="button" @click="openNew">
        + New address
      </button>
    </header>

    <div v-if="!items.length && !showForm" class="empty muted">
      No saved addresses. Add one to continue.
    </div>

    <div v-if="items.length && !showForm" class="grid">
      <article
        v-for="addr in items"
        :key="addr.id"
        class="addr"
        :class="{ selected: selectedId === addr.id }"
      >
        <header class="addr-head">
          <strong>{{ addr.name || "Unnamed" }}</strong>
          <span v-if="addr.id === defaultBillingId && addressType === 'billing'" class="tag">
            default
          </span>
          <span v-if="addr.id === defaultShippingId && addressType === 'shipping'" class="tag">
            default
          </span>
        </header>
        <p>
          {{ addr.street }}<template v-if="addr.street2">, {{ addr.street2 }}</template><br />
          {{ addr.city }} {{ addr.zip }} {{ addr.state_name }}<br />
          {{ addr.country_name }}
        </p>
        <p class="muted small">
          <span v-if="addr.email">{{ addr.email }}</span>
          <span v-if="addr.phone"> · {{ addr.phone }}</span>
        </p>
        <footer class="actions">
          <button class="button primary tiny" type="button" @click="$emit('use', addr.id)">
            Use this
          </button>
          <button class="button ghost tiny" type="button" @click="edit(addr)">Edit</button>
          <button
            v-if="canSetDefault"
            class="button ghost tiny"
            type="button"
            @click="$emit('default', addr.id)"
          >
            Set default
          </button>
          <button class="button danger tiny" type="button" @click="$emit('delete', addr.id)">
            Delete
          </button>
        </footer>
      </article>
    </div>

    <AddressForm
      v-if="showForm"
      :title="editing ? 'Edit address' : 'New address'"
      :address-type="addressType"
      :initial="editing"
      cancelable
      :submit-label="editing ? 'Update address' : 'Save address'"
      @submit="onSubmit"
      @cancel="closeForm"
    />
  </section>
</template>

<script setup>
import { ref } from "vue";

import AddressForm from "./AddressForm.vue";

const props = defineProps({
  title: { type: String, default: "Address book" },
  addressType: { type: String, default: "billing" },
  items: { type: Array, default: () => [] },
  selectedId: { type: Number, default: null },
  defaultBillingId: { type: Number, default: null },
  defaultShippingId: { type: Number, default: null },
  canSetDefault: { type: Boolean, default: true }
});

const emit = defineEmits(["use", "delete", "default", "save"]);

const showForm = ref(false);
const editing = ref(null);

function openNew() {
  editing.value = null;
  showForm.value = true;
}

function edit(addr) {
  editing.value = { ...addr };
  showForm.value = true;
}

function closeForm() {
  showForm.value = false;
  editing.value = null;
}

function onSubmit(payload) {
  emit("save", { ...payload, addressType: props.addressType });
  closeForm();
}
</script>

<style scoped>
.picker {
  padding: 1rem;
  display: grid;
  gap: 0.9rem;
}

.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

h3 {
  margin: 0;
}

.empty {
  padding: 1rem;
  border: 1px dashed var(--line);
  border-radius: 12px;
}

.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 0.7rem;
}

.addr {
  border: 1px solid var(--line);
  border-radius: 12px;
  padding: 0.8rem;
  display: grid;
  gap: 0.5rem;
}

.addr.selected {
  border-color: var(--accent);
  background: var(--accent-soft, #f0f7f4);
}

.addr-head {
  display: flex;
  align-items: center;
  gap: 0.4rem;
}

.tag {
  background: var(--accent, #2f7d63);
  color: white;
  font-size: 0.7rem;
  padding: 0.1rem 0.4rem;
  border-radius: 999px;
}

.addr p {
  margin: 0;
  line-height: 1.4;
  font-size: 0.9rem;
}

.small {
  font-size: 0.8rem;
}

.actions {
  display: flex;
  flex-wrap: wrap;
  gap: 0.35rem;
  margin-top: 0.3rem;
}

.button.tiny {
  padding: 0.25rem 0.55rem;
  font-size: 0.78rem;
}

.button.danger {
  color: var(--danger);
}
</style>
