<script setup>
import {
  ClipboardList,
  Cog,
  PackageCheck,
  Boxes,
  TrendingUp,
} from "lucide-vue-next";

import { summaryCards as defaultSummaryCards } from "../../data/manufacturingData.js";

const props = defineProps({
  cards: { type: Array, default: () => defaultSummaryCards },
  loading: { type: Boolean, default: false },
});

const emit = defineEmits(["select"]);

function selectMetric(card) {
  emit("select", card);
}

function onKeydown(event, card) {
  if (event.key === "Enter" || event.key === " ") {
    event.preventDefault();
    selectMetric(card);
  }
}

const icons = {
  purple: ClipboardList,
  blue: Cog,
  green: PackageCheck,
  orange: Boxes,
};

const iconStyles = {
  purple: "kpi-icon-purple",
  blue: "kpi-icon-blue",
  green: "kpi-icon-green",
  orange: "kpi-icon-orange",
};
</script>

<template>
  <section class="kpi-grid">
    <article
      v-for="card in cards"
      :key="card.title"
      class="kpi-card"
      :class="{ 'kpi-card--clickable': card.list }"
      :role="card.list ? 'button' : undefined"
      :tabindex="card.list ? 0 : undefined"
      @click="card.list && selectMetric(card)"
      @keydown="card.list && onKeydown($event, card)"
    >
      <div class="kpi-card-main">
        <div class="kpi-card-content">
          <p class="kpi-title">{{ card.title }}</p>
          <p v-if="loading" class="kpi-value kpi-value--loading">
            <span class="skeleton-block"></span>
          </p>
          <p v-else class="kpi-value">{{ card.value }}</p>
          <p class="kpi-description">{{ card.description }}</p>
        </div>

        <div class="kpi-icon" :class="iconStyles[card.color]">
          <component :is="icons[card.color] || ClipboardList" :size="19" />
        </div>
      </div>

      <div class="kpi-footer">
        <TrendingUp :size="14" />
        <span>View details</span>
      </div>

      <div class="kpi-bottom-border"></div>
    </article>
  </section>
</template>

<style>
.kpi-grid {
  display: grid;
  grid-template-columns: repeat(4, minmax(0, 1fr));
  gap: 12px;
  width: 100%;
  min-width: 0;
}

.kpi-card {
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-width: 0;
  padding: 12px 14px 10px;
  overflow: hidden;
  background: #ffffff;
  border: 1px solid #e1e6f2;
  border-radius: 11px;
  box-shadow: 0 2px 7px rgb(31 41 55 / 5%);
  transition:
    box-shadow 0.18s ease,
    transform 0.18s ease,
    border-color 0.18s ease;
}

.kpi-card--clickable {
  cursor: pointer;
}

.kpi-card--clickable:hover {
  transform: translateY(-1px);
}

.kpi-card--clickable:focus-visible {
  outline: 2px solid #493b91;
  outline-offset: 2px;
}

.kpi-card-main {
  display: flex;
  flex-direction: row;
  align-items: flex-start;
  justify-content: space-between;
  gap: 8px;
  min-width: 0;
}

.kpi-card-content {
  flex: 1 1 auto;
  min-width: 0;
}

.kpi-title {
  margin: 0;
  color: #78809b;
  font-size: 12px;
  font-weight: 500;
  line-height: 1.5;
  overflow-wrap: break-word;
}

.kpi-value {
  margin: 5px 0 0;
  color: #17153c;
  font-size: 21px;
  font-weight: 650;
  line-height: 1.3;
  letter-spacing: -0.5px;
  overflow-wrap: anywhere;
}

.kpi-value--loading {
  width: 72%;
  height: 22px;
  margin-top: 5px;
}

.skeleton-block {
  display: block;
  width: 100%;
  height: 100%;
  background: rgb(255 255 255 / 22%);
  border-radius: 6px;
  animation: kpi-pulse 1.2s ease-in-out infinite;
}

@keyframes kpi-pulse {
  0%,
  100% {
    opacity: 1;
  }

  50% {
    opacity: 0.5;
  }
}

.kpi-description {
  margin: 3px 0 0;
  color: #78809b;
  font-size: 11px;
  line-height: 1.45;
  overflow-wrap: break-word;
}

.kpi-icon {
  display: flex;
  flex: 0 0 34px;
  align-items: center;
  justify-content: center;
  width: 34px;
  height: 34px;
  border-radius: 9px;
}

.kpi-icon-purple {
  color: #6d28d9;
  background: #f3eefe;
}

.kpi-icon-blue {
  color: #2563eb;
  background: #eff6ff;
}

.kpi-icon-green {
  color: #059669;
  background: #ecfdf5;
}

.kpi-icon-orange {
  color: #c2410c;
  background: #fff7ed;
}

.kpi-footer {
  display: flex;
  align-items: center;
  gap: 7px;
  margin-top: 8px;
  padding-top: 6px;
  color: #78809b;
  font-size: 12px;
  line-height: 1.4;
  border-top: 1px solid #edf0f7;
}

.kpi-footer svg {
  flex-shrink: 0;
  color: #6040c5;
}

.kpi-bottom-border {
  position: absolute;
  right: 0;
  bottom: 0;
  left: 0;
  height: 3px;
  background: linear-gradient(90deg, #493b91, #c43f9d);
}

@media (max-width: 1200px) {
  .kpi-grid {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
}

@media (max-width: 600px) {
  .kpi-grid {
    grid-template-columns: minmax(0, 1fr);
    gap: 10px;
  }

  .kpi-card {
    padding: 11px;
  }

  .kpi-value {
    font-size: 19px;
  }
}
</style>
