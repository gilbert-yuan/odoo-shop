<template>
  <div v-if="visible" class="announcement" :style="{ background: bg, color: fg }">
    <div class="container row">
      <div class="messages">
        <transition name="fade" mode="out-in">
          <span :key="index" class="msg">{{ messages[index] }}</span>
        </transition>
      </div>
      <button class="close" type="button" aria-label="Dismiss" @click="close">✕</button>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted, ref } from "vue";

const STORAGE_KEY = "nextpept_announcement_dismissed";

const props = defineProps({
  bg: { type: String, default: "#0d8066" },
  fg: { type: String, default: "#fff" },
  messages: {
    type: Array,
    default: () => [
      "✦ Free shipping on orders over $99 — worldwide tracked delivery",
      "🧪 Every batch tested by 3rd-party lab — find COA via lot number",
      "🎁 New customer? 10% off your first order with code WELCOME10"
    ]
  },
  interval: { type: Number, default: 4500 }
});

const visible = ref(true);
const index = ref(0);
let timer = null;

onMounted(() => {
  if (typeof window !== "undefined" && localStorage.getItem(STORAGE_KEY) === "1") {
    visible.value = false;
    return;
  }
  if (props.messages.length > 1) {
    timer = setInterval(() => {
      index.value = (index.value + 1) % props.messages.length;
    }, props.interval);
  }
});

onUnmounted(() => {
  if (timer) clearInterval(timer);
});

function close() {
  visible.value = false;
  try {
    localStorage.setItem(STORAGE_KEY, "1");
  } catch {
    /* ignore */
  }
}
</script>

<style scoped>
.announcement {
  font-size: 0.86rem;
  font-weight: 500;
  line-height: 1.2;
}

.row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.8rem;
  min-height: 36px;
  padding: 0.4rem 0;
}

.messages {
  flex: 1;
  display: flex;
  justify-content: center;
  overflow: hidden;
}

.msg {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.close {
  background: transparent;
  border: 0;
  color: inherit;
  font-size: 0.95rem;
  cursor: pointer;
  opacity: 0.75;
  padding: 0.2rem 0.5rem;
}

.close:hover {
  opacity: 1;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.4s, transform 0.4s;
}

.fade-enter-from {
  opacity: 0;
  transform: translateY(8px);
}

.fade-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}

@media (max-width: 540px) {
  .announcement {
    font-size: 0.78rem;
  }
}
</style>
