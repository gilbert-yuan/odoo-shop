<template>
  <section v-if="attributeLines.length" class="variants">
    <div v-for="line in attributeLines" :key="line.id" class="line">
      <h4>{{ line.attribute_name }}</h4>
      <div
        class="options"
        :class="{
          swatches: line.display_type === 'color',
          radio: line.display_type === 'radio',
          select: line.display_type === 'select'
        }"
      >
        <template v-if="line.display_type === 'select'">
          <select :value="selected[line.attribute_id] || ''" @change="pick(line.attribute_id, $event.target.value)">
            <option value="" disabled>Choose {{ line.attribute_name }}</option>
            <option v-for="v in line.values" :key="v.ptav_id" :value="v.ptav_id">
              {{ v.name }}<span v-if="v.price_extra"> (+{{ money(v.price_extra) }})</span>
            </option>
          </select>
        </template>
        <template v-else>
          <button
            v-for="v in line.values"
            :key="v.ptav_id"
            type="button"
            class="opt"
            :class="{ active: selected[line.attribute_id] === v.ptav_id }"
            :style="line.display_type === 'color' && v.html_color ? { background: v.html_color } : {}"
            :title="v.name"
            @click="pick(line.attribute_id, v.ptav_id)"
          >
            <span v-if="line.display_type !== 'color'">{{ v.name }}</span>
            <span v-if="v.price_extra && line.display_type !== 'color'" class="extra">
              +{{ money(v.price_extra) }}
            </span>
          </button>
        </template>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, reactive, watch } from "vue";

const props = defineProps({
  attributeLines: { type: Array, default: () => [] },
  modelValue: { type: Array, default: () => [] },
  currency: { type: String, default: "USD" }
});

const emit = defineEmits(["update:modelValue"]);

const selected = reactive({});

watch(
  () => props.attributeLines,
  (lines) => {
    Object.keys(selected).forEach((k) => delete selected[k]);
    lines.forEach((line) => {
      const first = line.values?.[0];
      if (first) {
        selected[line.attribute_id] = first.ptav_id;
      }
    });
    emit("update:modelValue", Object.values(selected));
  },
  { immediate: true }
);

function pick(attributeId, ptavId) {
  selected[attributeId] = Number(ptavId);
  emit("update:modelValue", Object.values(selected));
}

function money(value) {
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: props.currency
  }).format(Number(value || 0));
}

defineExpose({ selected: computed(() => ({ ...selected })) });
</script>

<style scoped>
.variants {
  display: grid;
  gap: 0.7rem;
}

.line {
  display: grid;
  gap: 0.35rem;
}

h4 {
  margin: 0;
  font-size: 0.85rem;
  color: var(--muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.options {
  display: flex;
  gap: 0.45rem;
  flex-wrap: wrap;
}

.options select {
  border: 1px solid var(--line);
  background: #fff;
  border-radius: var(--radius-sm);
  padding: 0.6rem 0.8rem;
  font: inherit;
  min-width: 180px;
}

.opt {
  border: 1px solid var(--line);
  background: #fff;
  border-radius: 999px;
  padding: 0.45rem 0.85rem;
  cursor: pointer;
  font: inherit;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  transition: border-color 0.15s, transform 0.15s;
}

.opt:hover {
  border-color: var(--accent);
}

.opt.active {
  border-color: var(--accent);
  background: var(--accent-soft);
  font-weight: 600;
}

.swatches .opt {
  width: 28px;
  height: 28px;
  padding: 0;
  border-radius: 50%;
  border-width: 2px;
}

.swatches .opt.active {
  outline: 2px solid var(--accent);
  outline-offset: 2px;
}

.extra {
  color: var(--muted);
  font-size: 0.78rem;
}
</style>
