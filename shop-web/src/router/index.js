import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import CatalogPage from "../views/CatalogPage.vue";
import ProductPage from "../views/ProductPage.vue";
import CartPage from "../views/CartPage.vue";
import CheckoutPage from "../views/CheckoutPage.vue";
import AccountPage from "../views/AccountPage.vue";
import OrdersPage from "../views/OrdersPage.vue";
import WishlistPage from "../views/WishlistPage.vue";
import ComparePage from "../views/ComparePage.vue";
import NotFoundPage from "../views/NotFoundPage.vue";

const routes = [
  {
    path: "/",
    name: "home",
    component: HomePage
  },
  {
    path: "/shop",
    name: "catalog",
    component: CatalogPage
  },
  {
    path: "/product/:id",
    name: "product",
    component: ProductPage,
    props: true
  },
  {
    path: "/cart",
    name: "cart",
    component: CartPage
  },
  {
    path: "/checkout",
    name: "checkout",
    component: CheckoutPage
  },
  {
    path: "/account",
    name: "account",
    component: AccountPage
  },
  {
    path: "/account/orders",
    name: "orders",
    component: OrdersPage
  },
  {
    path: "/wishlist",
    name: "wishlist",
    component: WishlistPage
  },
  {
    path: "/compare",
    name: "compare",
    component: ComparePage
  },
  {
    path: "/:pathMatch(.*)*",
    name: "not-found",
    component: NotFoundPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0, behavior: "smooth" };
  }
});

export default router;
