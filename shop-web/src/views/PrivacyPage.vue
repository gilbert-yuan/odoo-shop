<template>
  <StaticPage
    title="Privacy Policy"
    description="How NextPept collects, uses, and protects your personal data."
  >
    <p>
      NextPept respects your privacy. This policy explains what data we collect, why we collect
      it, and how we protect it. Replace this placeholder with the version that has been
      reviewed against applicable laws (GDPR / CCPA / PIPL etc.).
    </p>
    <h2>Data we collect</h2>
    <ul>
      <li>Account details: name, email, phone, billing and shipping addresses.</li>
      <li>Order history and payment metadata (we do not store full card numbers).</li>
      <li>Technical data: IP address, browser type, device, cookies for cart and session.</li>
    </ul>
    <h2>How we use your data</h2>
    <ul>
      <li>To process orders, payments, and shipping.</li>
      <li>To send order confirmations and customer support messages.</li>
      <li>To improve the storefront and prevent fraud.</li>
    </ul>
    <h2>Sharing</h2>
    <p>
      We share data only with the payment processors, shipping carriers, and tax authorities
      required to fulfil your order. We never sell personal data.
    </p>
    <h2>Your rights</h2>
    <p>
      You may request access, correction, or deletion of your personal data at any time by
      contacting <a href="mailto:privacy@nextpept.com">privacy@nextpept.com</a>.
    </p>
    <h2>Cookies</h2>
    <p>
      The storefront uses essential cookies for cart and session persistence and optional
      cookies for analytics. You can clear cookies at any time in your browser settings.
    </p>
  </StaticPage>
</template>

<script setup>
import StaticPage from "./StaticPage.vue";
</script>
