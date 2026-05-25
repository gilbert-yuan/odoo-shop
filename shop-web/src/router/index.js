import { createRouter, createWebHistory } from "vue-router";

import HomePage from "../views/HomePage.vue";
import CatalogPage from "../views/CatalogPage.vue";
import ProductPage from "../views/ProductPage.vue";
import CartPage from "../views/CartPage.vue";
import CheckoutPage from "../views/CheckoutPage.vue";
import CheckoutDonePage from "../views/CheckoutDonePage.vue";
import AccountPage from "../views/AccountPage.vue";
import OrdersPage from "../views/OrdersPage.vue";
import OrderDetailPage from "../views/OrderDetailPage.vue";
import RegisterPage from "../views/RegisterPage.vue";
import PasswordForgotPage from "../views/PasswordForgotPage.vue";
import PasswordResetPage from "../views/PasswordResetPage.vue";
import ProfilePage from "../views/ProfilePage.vue";
import WishlistPage from "../views/WishlistPage.vue";
import ComparePage from "../views/ComparePage.vue";
import AboutPage from "../views/AboutPage.vue";
import TermsPage from "../views/TermsPage.vue";
import ShippingReturnsPage from "../views/ShippingReturnsPage.vue";
import RefundPolicyPage from "../views/RefundPolicyPage.vue";
import PrivacyPage from "../views/PrivacyPage.vue";
import FaqPage from "../views/FaqPage.vue";
import ContactPage from "../views/ContactPage.vue";
import WholesalePage from "../views/WholesalePage.vue";
import CoaPage from "../views/CoaPage.vue";
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
    path: "/checkout/done/:orderId",
    name: "checkout-done",
    component: CheckoutDonePage,
    props: true
  },
  {
    path: "/account",
    name: "account",
    component: AccountPage
  },
  {
    path: "/account/register",
    name: "register",
    component: RegisterPage
  },
  {
    path: "/account/forgot",
    name: "password-forgot",
    component: PasswordForgotPage
  },
  {
    path: "/account/reset",
    name: "password-reset",
    component: PasswordResetPage
  },
  {
    path: "/account/profile",
    name: "profile",
    component: ProfilePage
  },
  {
    path: "/account/orders",
    name: "orders",
    component: OrdersPage
  },
  {
    path: "/account/orders/:id",
    name: "order-detail",
    component: OrderDetailPage,
    props: true
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
    path: "/about",
    name: "about",
    component: AboutPage
  },
  {
    path: "/terms",
    name: "terms",
    component: TermsPage
  },
  {
    path: "/shipping-returns",
    name: "shipping-returns",
    component: ShippingReturnsPage
  },
  {
    path: "/refund-policy",
    name: "refund-policy",
    component: RefundPolicyPage
  },
  {
    path: "/privacy",
    name: "privacy",
    component: PrivacyPage
  },
  {
    path: "/faq",
    name: "faq",
    component: FaqPage
  },
  {
    path: "/contact",
    name: "contact",
    component: ContactPage
  },
  {
    path: "/wholesale",
    name: "wholesale",
    component: WholesalePage
  },
  {
    path: "/coa",
    name: "coa",
    component: CoaPage
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
