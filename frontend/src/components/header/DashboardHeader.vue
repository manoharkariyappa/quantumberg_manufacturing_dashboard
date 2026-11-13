<script setup>
import { computed } from "vue";
import {
  Building2,
  CalendarDays,
  ChevronDown,
  Factory,
  RefreshCw,
} from "lucide-vue-next";

const props = defineProps({
  companies: { type: Array, default: () => [] },
  company: { type: String, default: "" },
  fromDate: { type: String, default: "" },
  toDate: { type: String, default: "" },
  loading: { type: Boolean, default: false },
});

const emit = defineEmits(["company-change", "date-change", "refresh"]);

const selectedCompany = computed({
  get: () => props.company,
  set: (value) => emit("company-change", value),
});

const selectedFromDate = computed({
  get: () => props.fromDate,
  set: (value) =>
    emit("date-change", { from_date: value, to_date: props.toDate }),
});

const selectedToDate = computed({
  get: () => props.toDate,
  set: (value) =>
    emit("date-change", { from_date: props.fromDate, to_date: value }),
});
</script>

<template>
  <header class="dashboard-header qb-card">
    <div class="dashboard-header-title">
      <div class="dashboard-header-icon">
        <Factory :size="19" />
      </div>

      <div class="min-w-0">
        <h1>Production Overview</h1>
        <p>Monitor work orders, production output and quality</p>
      </div>
    </div>

    <div class="dashboard-header-controls">
      <label
        v-if="companies.length"
        class="dashboard-control dashboard-control--company"
      >
        <span class="dashboard-control-icon"><Building2 :size="14" /></span>
        <select v-model="selectedCompany" aria-label="Company">
          <option
            v-for="companyOption in companies"
            :key="companyOption.name"
            :value="companyOption.name"
          >
            {{ companyOption.name }}
          </option>
        </select>
        <ChevronDown :size="13" class="dashboard-control-chevron" />
      </label>

      <label class="dashboard-control">
        <span class="dashboard-control-icon"><CalendarDays :size="14" /></span>
        <span class="dashboard-control-label">From</span>
        <input
          v-model="selectedFromDate"
          type="date"
          aria-label="From date"
          :max="toDate"
        />
      </label>

      <label class="dashboard-control">
        <span class="dashboard-control-icon"><CalendarDays :size="14" /></span>
        <span class="dashboard-control-label">To</span>
        <input
          v-model="selectedToDate"
          type="date"
          aria-label="To date"
          :min="fromDate"
        />
      </label>

      <button
        type="button"
        class="dashboard-button"
        :disabled="loading"
        @click="emit('refresh')"
      >
        <RefreshCw :size="14" :class="{ 'dashboard-spin': loading }" />
        {{ loading ? "Loading" : "Refresh" }}
      </button>
    </div>
  </header>
</template>

<style scoped>
.dashboard-header {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  padding: 12px 16px;
}

.dashboard-header-title {
  display: flex;
  flex: 1 1 0;
  min-width: 150px;
  align-items: center;
  gap: 11px;
}

.dashboard-header-icon {
  display: grid;
  flex: 0 0 40px;
  width: 40px;
  height: 40px;
  color: #ffffff;
  background: linear-gradient(135deg, #493b91, #c43f9d);
  border-radius: 10px;
  place-items: center;
  box-shadow: 0 4px 10px rgb(73 59 145 / 22%);
}

.dashboard-header-title h1 {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dashboard-header-title p {
  margin: 3px 0 0;
  overflow: hidden;
  color: var(--text-muted, #78809b);
  font-size: 12px;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.dashboard-header-controls {
  display: flex;
  flex: 0 0 auto;
  flex-wrap: nowrap;
  min-width: 0;
  align-items: center;
  justify-content: flex-end;
  gap: 6px;
  margin-left: auto;
  white-space: nowrap;
}

.dashboard-header-controls .dashboard-button {
  gap: 6px;
  padding: 0 9px;
}

.dashboard-control {
  display: inline-flex;
  flex-shrink: 0;
  height: 34px;
  min-width: 0;
  align-items: center;
  gap: 6px;
  padding: 0 8px;
  margin: 0;
  line-height: 1;
  background: var(--card-bg, #ffffff);
  border: 1px solid var(--border-color, #e1e6f2);
  border-radius: 7px;
}

.dashboard-control--company {
  max-width: 220px;
}

.dashboard-control-icon {
  display: inline-flex;
  flex-shrink: 0;
  color: #6040c5;
}

.dashboard-control-label {
  color: var(--text-muted, #78809b);
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 0.3px;
  text-transform: uppercase;
}

.dashboard-control select,
.dashboard-control input {
  min-width: 0;
  height: 100%;
  padding: 0;
  color: var(--text-color, #333333);
  font-size: 12px;
  font-weight: 500;
  background: transparent;
  border: 0;
  outline: none;
}

.dashboard-control select {
  width: 100%;
  cursor: pointer;
  appearance: none;
  padding-right: 2px;
}

.dashboard-control input {
  width: 100px;
  color-scheme: light;
}

.dashboard-control input::-webkit-calendar-picker-indicator {
  margin: 0;
  padding: 0;
  cursor: pointer;
  opacity: 0.7;
}

.dashboard-control-chevron {
  flex-shrink: 0;
  color: var(--text-muted, #78809b);
  pointer-events: none;
}

.dashboard-spin {
  animation: dashboard-spin 0.9s linear infinite;
}

@keyframes dashboard-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1240px) {
  .dashboard-header-title {
    min-width: 100%;
  }

  .dashboard-header-controls {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    width: 100%;
    margin-left: 0;
    white-space: normal;
  }

  .dashboard-control--company {
    grid-column: span 2;
    max-width: none;
    width: 100%;
  }

  .dashboard-control {
    width: 100%;
  }

  .dashboard-control input {
    width: 100%;
  }

  .dashboard-button {
    grid-column: span 2;
    width: 100%;
  }
}

@media (max-width: 760px) {
  .dashboard-header-controls {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }

  .dashboard-control--company {
    grid-column: span 2;
  }

  .dashboard-button {
    grid-column: span 1;
  }
}

@media (max-width: 600px) {
  .dashboard-header {
    padding: 12px;
  }

  .dashboard-header-title h1 {
    font-size: 17px;
  }
}
</style>
