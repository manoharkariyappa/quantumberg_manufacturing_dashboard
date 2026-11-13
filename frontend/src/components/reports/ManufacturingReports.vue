<script setup>
import { FileText, ArrowUpRight } from "lucide-vue-next";
import { manufacturingReports } from "../../data/manufacturingData.js";
</script>

<template>
  <section class="qb-card report-library mt-5 overflow-hidden rounded-lg border border-qb-border bg-white shadow-sm">
    <div class="report-library-header flex items-center justify-between border-b border-slate-100 px-4 py-3">
      <div>
        <h2 class="text-sm font-semibold text-qb-text">Manufacturing Reports</h2>
        <p class="mt-1 text-xs text-qb-muted">Quick overview of manufacturing reports</p>
      </div>
      <FileText :size="18" class="text-qb-purple" />
    </div>

    <div class="grid grid-cols-1 gap-0 sm:grid-cols-2 xl:grid-cols-3">
      <button
        v-for="report in manufacturingReports"
        :key="report.title"
        type="button"
        class="flex min-w-0 items-center gap-3 border-b border-slate-100 p-4 text-left transition hover:bg-violet-50/50 sm:even:border-l sm:even:border-slate-100 xl:[&:nth-child(3n+2)]:border-l xl:[&:nth-child(3n+3)]:border-l"
        :title="`${report.title} (demo data)`"
        @click="$emit('report-click', report)"
      >
        <span class="grid h-9 w-9 shrink-0 place-items-center rounded-lg bg-violet-50 text-qb-purple">
          <FileText :size="17" />
        </span>

        <span class="min-w-0 flex-1">
          <span class="block text-xs font-semibold text-qb-text">{{ report.title }}</span>
          <span class="mt-1 block text-xs text-qb-muted">{{ report.description }}</span>
          <span class="mt-2 block text-xs font-medium text-qb-purple">{{ report.count }} records · Demo</span>
        </span>

        <ArrowUpRight :size="15" class="shrink-0 text-qb-muted" />
      </button>
    </div>
  </section>
</template>
