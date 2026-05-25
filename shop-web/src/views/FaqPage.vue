<template>
  <StaticPage
    title="Frequently Asked Questions"
    description="Common questions about NextPept products, ordering, shipping, and research use."
  >
    <div class="faq">
      <details v-for="(item, idx) in items" :key="idx" class="item">
        <summary>{{ item.q }}</summary>
        <div class="answer" v-html="item.a"></div>
      </details>
    </div>
  </StaticPage>
</template>

<script setup>
import StaticPage from "./StaticPage.vue";

const items = [
  {
    q: "Are NextPept products approved for human use?",
    a: "No. All products are sold strictly <strong>for laboratory research purposes</strong>. They are not intended for diagnostic, therapeutic, food, or cosmetic use, and may not be administered to humans or animals."
  },
  {
    q: "How is purity verified?",
    a: "Every batch is tested by an accredited third-party lab. The Certificate of Analysis (COA) including HPLC and mass spectrometry data can be retrieved via the <a href='/coa'>COA Lookup</a> page using the lot number printed on your vial."
  },
  {
    q: "How are products shipped?",
    a: "Domestic orders ship via tracked courier in 1–3 business days. International orders ship via tracked carrier, usually 5–10 business days. Cold-chain items use insulated packaging with cool packs."
  },
  {
    q: "Will I be charged customs or import duty?",
    a: "Possibly — duties and import taxes are determined by your destination country and are the buyer's responsibility. We declare contents truthfully as research chemicals."
  },
  {
    q: "What payment methods do you accept?",
    a: "Standard online providers configured by the store (card, PayPal, wire transfer). The methods available at checkout depend on your billing country."
  },
  {
    q: "Do you ship internationally?",
    a: "Yes, to most jurisdictions. Some regions have legal restrictions on specific peptides — orders may be cancelled at our discretion if a destination is restricted."
  },
  {
    q: "How do I store the peptides after receiving them?",
    a: "Unreconstituted lyophilised peptides should be kept at –20 °C in a sealed, light-protected container. After reconstitution, store at 2–8 °C and use within the period stated in the product data sheet."
  },
  {
    q: "Can I return or exchange a product?",
    a: "Sealed and unused items may be returned within 14 days. See the <a href='/refund-policy'>Refund &amp; Returns Policy</a> for the full procedure."
  },
  {
    q: "Do you offer wholesale or bulk pricing?",
    a: "Yes. Submit the <a href='/wholesale'>Wholesale Inquiry</a> form and our team will reply within 1–2 business days with a custom quote."
  },
  {
    q: "How do I track my order?",
    a: "Once your order ships, a tracking number is emailed to you and is also visible on the <a href='/account/orders'>Orders</a> page if you have an account."
  },
  {
    q: "What if I have not received an order confirmation email?",
    a: "Check your spam folder first. Still missing? Reach us through the <a href='/contact'>Contact</a> page with the email used at checkout — we will resend it."
  }
];
</script>

<style scoped>
.faq {
  display: grid;
  gap: 0.55rem;
}

.item {
  border: 1px solid var(--line);
  border-radius: var(--radius-md);
  background: var(--panel);
  padding: 0 1rem;
  transition: border-color 0.15s;
}

.item[open] {
  border-color: var(--accent);
}

summary {
  cursor: pointer;
  padding: 0.85rem 0;
  font-weight: 600;
  list-style: none;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

summary::after {
  content: "+";
  font-size: 1.2rem;
  color: var(--muted);
  transition: transform 0.15s;
}

.item[open] summary::after {
  content: "−";
  color: var(--accent);
}

summary::-webkit-details-marker {
  display: none;
}

.answer {
  padding: 0 0 0.95rem;
  line-height: 1.6;
  color: var(--muted);
}

.answer :deep(strong) {
  color: var(--ink);
}

.answer :deep(a) {
  color: var(--accent);
}
</style>
