<script setup>
import { computed, onMounted, ref } from "vue";
import DashboardHeader from "../components/header/DashboardHeader.vue";
import SummaryCards from "../components/cards/SummaryCards.vue";

import WorkOrderAnalysis from "../components/charts/WorkOrderAnalysis.vue";
import JobCardAnalysis from "../components/charts/JobCardAnalysis.vue";
import ProducedQuantity from "../components/charts/ProducedQuantity.vue";
import CompletedOperation from "../components/charts/CompletedOperation.vue";
import WorkOrderQuantity from "../components/charts/WorkOrderQuantity.vue";
import PendingWorkOrder from "../components/charts/PendingWorkOrder.vue";
import QualityInspection from "../components/charts/QualityInspection.vue";
import DowntimeAnalysis from "../components/charts/DowntimeAnalysis.vue";

import ManufacturingReports from "../components/reports/ManufacturingReports.vue";

import { summaryCards as defaultSummaryCards } from "../data/manufacturingData.js";
import { getList, openList } from "../services/api.js";
import { fetchDashboardData } from "../services/dashboard.js";

const companies = ref([]);
const company = ref("");
const fromDate = ref("");
const toDate = ref("");
const loading = ref(true);
const error = ref("");

const summary = ref(null);
const workOrderAnalysis = ref(null);
const jobCardAnalysis = ref(null);
const producedQuantity = ref(null);
const completedOperation = ref(null);
const workOrderQuantity = ref(null);
const pendingWorkOrder = ref(null);
const qualityInspection = ref(null);
const downtimeAnalysis = ref(null);

function getFrappe() {
  return window.frappe;
}

function isoDate(date) {
  return date.toISOString().slice(0, 10);
}

function fallbackFromDate() {
  const date = new Date();
  date.setDate(date.getDate() - 30);
  return isoDate(date);
}

function formatCurrency(value) {
  return new Intl.NumberFormat("en-IN", {
    style: "currency",
    currency: "INR",
    maximumFractionDigits: 0,
  }).format(Number(value) || 0);
}

const summaryCards = computed(() => {
  const data = summary.value;

  return defaultSummaryCards.map((card) => {
    if (!data) {
      return {
        ...card,
        value: card.format === "currency" ? formatCurrency(0) : 0,
      };
    }

    const rawValue = data[card.valueKey];
    const value =
      card.format === "currency"
        ? formatCurrency(rawValue)
        : Number(rawValue) || 0;

    return { ...card, value };
  });
});

async function loadCompanies() {
  try {
    const list = await getList("Company", {
      fields: ["name"],
      order_by: "name asc",
      limit_page_length: 0,
    });

    companies.value = (list || []).map((row) => ({ name: row.name }));

    if (
      companies.value.length &&
      !companies.value.some((item) => item.name === company.value)
    ) {
      company.value = companies.value[0].name;
    }
  } catch {
    companies.value = [];
  }
}

async function loadDashboard() {
  if (!fromDate.value || !toDate.value) {
    return;
  }

  loading.value = true;
  error.value = "";

  try {
    const data = await fetchDashboardData({
      from_date: fromDate.value,
      to_date: toDate.value,
      company: company.value || null,
    });

    summary.value = data.summary;
    workOrderAnalysis.value = data.workOrderAnalysis;
    jobCardAnalysis.value = data.jobCardAnalysis;
    producedQuantity.value = data.producedQuantity;
    completedOperation.value = data.completedOperation;
    workOrderQuantity.value = data.workOrderQuantity;
    pendingWorkOrder.value = data.pendingWorkOrder;
    qualityInspection.value = data.qualityInspection;
    downtimeAnalysis.value = data.downtimeAnalysis;
  } catch (err) {
    error.value = err?.message || "Unable to load dashboard data.";
  } finally {
    loading.value = false;
  }
}

function setCompany(value) {
  company.value = value;
  loadDashboard();
}

function setDateRange({ from_date, to_date }) {
  if (from_date) {
    fromDate.value = from_date;
  }

  if (to_date) {
    toDate.value = to_date;
  }

  loadDashboard();
}

onMounted(async () => {
  const frappe = getFrappe();
  const today = frappe?.datetime?.get_today?.() || isoDate(new Date());

  fromDate.value =
    frappe?.datetime?.add_days?.(today, -30) || fallbackFromDate();
  toDate.value = today;
  company.value = frappe?.defaults?.get_user_default?.("Company") || "";

  await loadCompanies();
  await loadDashboard();
});

function refreshDashboard() {
  loadDashboard();
}

function handleOpenMetric(card) {
  if (!card?.list) {
    return;
  }

  const filters = { ...(card.list.filters || {}) };

  if (company.value) {
    filters.company = company.value;
  }

  if (card.list.dateField && fromDate.value && toDate.value) {
    filters[card.list.dateField] = [
      "between",
      [fromDate.value, toDate.value],
    ];
  }

  openList(card.list.doctype, filters);
}

function handleReportClick(report) {
  window.alert(
    `${report.title}\n${report.description}\nRecords: ${report.count}\n\nDemo data only.`,
  );
}
</script>

<template>
  <main class="manufacturing-dashboard">
    <DashboardHeader
      :companies="companies"
      :company="company"
      :from-date="fromDate"
      :to-date="toDate"
      :loading="loading"
      @company-change="setCompany"
      @date-change="setDateRange"
      @refresh="refreshDashboard"
    />

    <p v-if="error" class="manufacturing-error">{{ error }}</p>

    <section class="manufacturing-summary">
      <SummaryCards
        :cards="summaryCards"
        :loading="loading"
        @select="handleOpenMetric"
      />
    </section>

    <section class="manufacturing-charts">
      <WorkOrderAnalysis :data="workOrderAnalysis" />
      <JobCardAnalysis :data="jobCardAnalysis" />
      <ProducedQuantity :data="producedQuantity" />
      <CompletedOperation :data="completedOperation" />
      <WorkOrderQuantity :data="workOrderQuantity" />
      <PendingWorkOrder :data="pendingWorkOrder" />
      <QualityInspection :data="qualityInspection" />
      <DowntimeAnalysis :data="downtimeAnalysis" />
    </section>

    <section class="manufacturing-reports">
      <ManufacturingReports @report-click="handleReportClick" />
    </section>
  </main>
</template>

<style>
.manufacturing-dashboard {
  width: 100%;
  min-width: 0;
  min-height: 100vh;
  padding: 12px;
  box-sizing: border-box;
  color: var(--text-color, #333333);
  font-family: var(--font-stack, inherit);
  font-size: 13px;
  line-height: 1.5;
}

.manufacturing-dashboard *,
.manufacturing-dashboard *::before,
.manufacturing-dashboard *::after {
  box-sizing: border-box;
}

.manufacturing-error {
  margin: 10px 0 0;
  padding: 8px 12px;
  color: #b42318;
  font-size: 12px;
  background: #fff1f0;
  border: 1px solid #ffd2cc;
  border-radius: 8px;
}

/* Summary section */
.manufacturing-summary {
  display: block;
  width: 100%;
  min-width: 0;
  margin-top: 12px;
}

/* Force KPI cards into a four-column layout */
.manufacturing-summary > * {
  width: 100%;
  min-width: 0;
}

.manufacturing-summary .grid {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 12px !important;
  width: 100%;
}

/* Force the chart grid layout */
.manufacturing-charts {
  display: grid !important;
  grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
  gap: 12px;
  align-items: stretch;
  width: 100%;
  min-width: 0;
  margin-top: 12px;
}

.manufacturing-charts > * {
  width: 100%;
  min-width: 0;
  height: 100%;
}

.manufacturing-reports {
  width: 100%;
  min-width: 0;
  margin-top: 16px;
}

/* Tablets and smaller desktop screens */
@media (max-width: 1200px) {
  .manufacturing-summary .grid {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }

  .manufacturing-charts {
    grid-template-columns: repeat(2, minmax(0, 1fr)) !important;
  }
}

/* Mobile */
@media (max-width: 650px) {
  .manufacturing-dashboard {
    padding: 8px;
  }

  .manufacturing-summary .grid,
  .manufacturing-charts {
    grid-template-columns: minmax(0, 1fr) !important;
    gap: 10px !important;
  }
}
</style>
