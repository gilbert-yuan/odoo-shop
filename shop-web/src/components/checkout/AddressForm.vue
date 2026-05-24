<template>
  <form class="card form" @submit.prevent="submit">
    <h3>{{ title }}</h3>
    <div class="grid two">
      <label>
        Full name
        <input v-model="local.name" class="input" required />
      </label>
      <label>
        Email
        <input v-model="local.email" class="input" type="email" required />
      </label>
      <label>
        Phone
        <input v-model="local.phone" class="input" />
      </label>
      <label>
        Country ID
        <input v-model.number="local.country_id" class="input" type="number" />
      </label>
      <label>
        Street
        <input v-model="local.street" class="input" required />
      </label>
      <label>
        Street 2
        <input v-model="local.street2" class="input" />
      </label>
      <label>
        City
        <input v-model="local.city" class="input" required />
      </label>
      <label>
        ZIP
        <input v-model="local.zip" class="input" required />
      </label>
      <label>
        State ID
        <input v-model.number="local.state_id" class="input" type="number" />
      </label>
      <label>
        VAT
        <input v-model="local.vat" class="input" />
      </label>
    </div>
    <button class="button primary" type="submit">
      Save {{ addressType }} address
    </button>
  </form>
</template>

<script setup>
import { reactive } from "vue";

const props = defineProps({
  title: {
    type: String,
    default: "Address"
  },
  addressType: {
    type: String,
    default: "billing"
  }
});

const emit = defineEmits(["submit"]);

const local = reactive({
  name: "",
  email: "",
  phone: "",
  country_id: null,
  street: "",
  street2: "",
  city: "",
  zip: "",
  state_id: null,
  vat: ""
});

function submit() {
  emit("submit", {
    addressType: props.addressType,
    form: { ...local }
  });
}
</script>

<style scoped>
.form {
  padding: 1rem;
  display: grid;
  gap: 0.9rem;
}

h3 {
  margin: 0;
}

.two {
  grid-template-columns: 1fr 1fr;
}

label {
  display: grid;
  gap: 0.35rem;
}

@media (max-width: 860px) {
  .two {
    grid-template-columns: 1fr;
  }
}
</style>
