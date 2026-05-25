<template>
  <article class="card skeleton">
    <div class="img shimmer"></div>
    <div class="body">
      <div class="line shimmer"></div>
      <div class="line short shimmer"></div>
      <div class="bottom">
        <div class="price shimmer"></div>
        <div class="btn shimmer"></div>
      </div>
    </div>
  </article>
</template>

<style scoped>
.skeleton {
  overflow: hidden;
  display: grid;
  grid-template-rows: 220px 1fr;
}

.img {
  background: linear-gradient(160deg, #ececec 0%, #f5f5f5 100%);
}

.body {
  padding: 1rem;
  display: grid;
  gap: 0.6rem;
}

.line {
  height: 0.95rem;
  border-radius: 6px;
  background: #ececec;
}

.line.short {
  width: 70%;
}

.bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.4rem;
}

.price {
  width: 70px;
  height: 1.2rem;
  border-radius: 6px;
  background: #ececec;
}

.btn {
  width: 64px;
  height: 1.8rem;
  border-radius: 999px;
  background: #ececec;
}

.shimmer {
  position: relative;
  overflow: hidden;
}

.shimmer::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(
    90deg,
    transparent 0%,
    rgba(255, 255, 255, 0.55) 50%,
    transparent 100%
  );
  animation: shimmer 1.4s infinite;
}

@keyframes shimmer {
  from {
    transform: translateX(-100%);
  }
  to {
    transform: translateX(100%);
  }
}
</style>
