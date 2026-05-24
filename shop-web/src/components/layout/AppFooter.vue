<template>
  <footer class="footer">
    <div class="container footer-grid">
      <section>
        <h3>Northstar Commerce</h3>
        <p class="muted">
          A modern Vue storefront connected to Odoo 18 ecommerce APIs.
        </p>
      </section>
      <section>
        <h4>Customer</h4>
        <RouterLink to="/shop">Shop</RouterLink>
        <RouterLink to="/cart">Cart</RouterLink>
        <RouterLink to="/account/orders">Orders</RouterLink>
      </section>
      <section>
        <h4>Commerce</h4>
        <RouterLink to="/wishlist">Wishlist</RouterLink>
        <RouterLink to="/compare">Compare</RouterLink>
        <RouterLink to="/checkout">Checkout</RouterLink>
      </section>
    </div>
  </footer>
</template>

<script setup>
import { RouterLink } from "vue-router";
</script>

<style scoped>
.footer {
  border-top: 1px solid var(--line);
  margin-top: 2rem;
  padding: 2.2rem 0;
  background: #f2eee3;
}

.footer-grid {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 1.2rem;
}

h3,
h4 {
  margin: 0 0 0.5rem;
}

section {
  display: grid;
  gap: 0.4rem;
}

section a {
  color: var(--muted);
}

@media (max-width: 820px) {
  .footer-grid {
    grid-template-columns: 1fr;
  }
}
</style>
