<script setup>
defineProps({
  title: { type: String, required: true },
  subtitle: { type: String, default: "" },
});
</script>

<template>
  <section class="qb-card chart-card min-w-0 overflow-hidden rounded-lg border border-qb-border bg-white shadow-sm">
    <div class="chart-card-header border-b border-slate-100 px-4 py-3">
      <h2 class="text-sm font-semibold leading-5 text-qb-text">{{ title }}</h2>
      <p v-if="subtitle" class="mt-1 text-xs leading-4 text-qb-muted">{{ subtitle }}</p>
    </div>
    <div class="min-w-0 p-3">
      <slot />
    </div>
  </section>
</template>
