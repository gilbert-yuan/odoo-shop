<template>
  <ol class="steps">
    <li
      v-for="(step, idx) in steps"
      :key="step.key"
      :class="{
        active: step.key === currentStep,
        done: doneSteps.includes(step.key),
        clickable: doneSteps.includes(step.key)
      }"
      @click="navigate(step.key)"
    >
      <span class="dot">{{ idx + 1 }}</span>
      <span class="label">{{ step.label }}</span>
    </li>
  </ol>
</template>

<script setup>
defineProps({
  currentStep: { type: String, required: true },
  doneSteps: { type: Array, default: () => [] }
});

const emit = defineEmits(["jump"]);

const steps = [
  { key: "address", label: "Address" },
  { key: "delivery", label: "Delivery" },
  { key: "payment", label: "Payment" }
];

function navigate(key) {
  emit("jump", key);
}
</script>

<style scoped>
.steps {
  list-style: none;
  margin: 0;
  padding: 0;
  display: flex;
  gap: 0.6rem;
  align-items: center;
  flex-wrap: wrap;
}

.steps li {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.4rem 0.8rem;
  border-radius: 999px;
  background: #f4f6f5;
  color: var(--muted);
  font-size: 0.88rem;
  user-select: none;
}

.steps li.active {
  background: var(--accent, #2f7d63);
  color: white;
}

.steps li.done {
  background: var(--accent-soft, #e2efe9);
  color: var(--accent, #2f7d63);
}

.steps li.clickable {
  cursor: pointer;
}

.dot {
  width: 1.4rem;
  height: 1.4rem;
  border-radius: 50%;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  background: rgba(255, 255, 255, 0.4);
  font-weight: 600;
  font-size: 0.78rem;
}

.steps li.active .dot {
  background: rgba(255, 255, 255, 0.25);
}

.steps li.done .dot {
  background: var(--accent, #2f7d63);
  color: white;
}
</style>
