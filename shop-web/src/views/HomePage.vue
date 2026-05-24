<template>
  <div class="container home">
    <section class="hero card rise-in">
      <div>
        <p class="eyebrow">Global-ready Odoo Storefront</p>
        <h1>Build premium ecommerce experiences on top of Odoo 18 APIs.</h1>
        <p class="muted">
          Headless Vue storefront with product discovery, cart, checkout, loyalty, wishlist, and compare flows.
        </p>
        <div class="hero-actions">
          <RouterLink class="button primary" to="/shop">Shop now</RouterLink>
          <RouterLink class="button ghost" to="/checkout">Go to checkout</RouterLink>
        </div>
      </div>
      <div class="hero-stat">
        <div>
          <strong>{{ cartStore.quantity }}</strong>
          <span>Items in cart</span>
        </div>
        <div>
          <strong>{{ compareStore.ids.length }}</strong>
          <span>In compare list</span>
        </div>
        <div>
          <strong>{{ wishlistStore.ids.length }}</strong>
          <span>Wishlist items</span>
        </div>
      </div>
    </section>

    <section class="grid showcase">
      <article class="card tile">
        <h3>Catalog and Search</h3>
        <p class="muted">Category, filters, sorting and instant product discovery backed by Odoo models.</p>
      </article>
      <article class="card tile">
        <h3>Checkout and Delivery</h3>
        <p class="muted">Address capture, shipping method selection and payment transaction initiation.</p>
      </article>
      <article class="card tile">
        <h3>Engagement Features</h3>
        <p class="muted">Wishlist, compare, stock alerts and loyalty coupons integrated in one UI.</p>
      </article>
    </section>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";

import { useCartStore } from "../stores/cart";
import { useCompareStore } from "../stores/compare";
import { useWishlistStore } from "../stores/wishlist";

const cartStore = useCartStore();
const compareStore = useCompareStore();
const wishlistStore = useWishlistStore();
</script>

<style scoped>
.home {
  display: grid;
  gap: 1.3rem;
  padding-top: 1.1rem;
}

.hero {
  padding: clamp(1rem, 3vw, 2rem);
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 1rem;
  background:
    radial-gradient(circle at 80% 10%, rgba(13, 128, 102, 0.18), transparent 30%),
    linear-gradient(160deg, #fffef7 0%, #f6fbf8 100%);
}

h1 {
  margin: 0.3rem 0 0.7rem;
  font-size: clamp(1.8rem, 3.2vw, 3rem);
  line-height: 1.08;
}

.eyebrow {
  margin: 0;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-size: 0.74rem;
  color: var(--muted);
  font-weight: 700;
}

.hero-actions {
  margin-top: 1rem;
  display: flex;
  gap: 0.6rem;
}

.hero-stat {
  display: grid;
  gap: 0.8rem;
  align-content: start;
}

.hero-stat div {
  background: #fff;
  border: 1px solid var(--line);
  border-radius: 16px;
  padding: 0.9rem;
  display: grid;
  gap: 0.2rem;
}

.hero-stat strong {
  font-size: 1.5rem;
}

.hero-stat span {
  color: var(--muted);
  font-size: 0.9rem;
}

.showcase {
  grid-template-columns: repeat(3, 1fr);
}

.tile {
  padding: 1rem;
}

.tile h3 {
  margin: 0;
}

.tile p {
  margin: 0.5rem 0 0;
}

@media (max-width: 960px) {
  .hero {
    grid-template-columns: 1fr;
  }

  .showcase {
    grid-template-columns: 1fr;
  }
}
</style>
