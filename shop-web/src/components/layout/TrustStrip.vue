<template>
  <section class="trust">
    <div class="container grid">
      <div v-for="item in items" :key="item.title" class="item">
        <span class="ic">{{ item.icon }}</span>
        <div class="txt">
          <strong>{{ item.title }}</strong>
          <span class="muted">{{ item.sub }}</span>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
const items = [
  { icon: "🚚", title: "Free worldwide shipping", sub: "On orders over $99" },
  { icon: "🧪", title: "Lab-tested authenticity", sub: "3rd-party COA per batch" },
  { icon: "🔒", title: "Secure checkout", sub: "Encrypted payments" },
  { icon: "↩️", title: "14-day returns", sub: "Hassle-free refunds" }
];
</script>

<style scoped>
.trust {
  border-top: 1px solid var(--line);
  border-bottom: 1px solid var(--line);
  background: var(--panel);
}

.grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  padding: 1.1rem 0;
}

.item {
  display: flex;
  align-items: center;
  gap: 0.7rem;
}

.ic {
  font-size: 1.5rem;
  flex-shrink: 0;
}

.txt {
  display: grid;
  line-height: 1.25;
}

.txt strong {
  font-size: 0.92rem;
}

.txt .muted {
  font-size: 0.8rem;
}

@media (max-width: 860px) {
  .grid {
    grid-template-columns: 1fr 1fr;
    gap: 0.9rem 1rem;
  }
}

@media (max-width: 460px) {
  .grid {
    grid-template-columns: 1fr;
  }
}
</style>
