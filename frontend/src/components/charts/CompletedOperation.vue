<script setup>
import { computed } from "vue";
import VueApexCharts from "vue3-apexcharts";
import ChartPanel from "./ChartPanel.vue";
import { completedOperation as demoCompletedOperation } from "../../data/manufacturingData.js";

const props = defineProps({
  data: { type: Object, default: null },
});

const chartData = computed(() => {
  const data = props.data;

  if (!data) {
    return {
      labels: demoCompletedOperation.categories,
      series: demoCompletedOperation.series[0]?.data || [],
    };
  }

  return {
    labels: data.labels || [],
    series: data.values || [],
  };
});

const options = computed(() => ({
  chart: {
    type: "donut",
    height: 210,
    toolbar: { show: false },
    fontFamily: "var(--font-stack, inherit)",
    animations: { enabled: true, speed: 350 },
  },
  colors: ["#493b91", "#3987f5", "#20bf88", "#c43f9d", "#ffad19", "#8b83c9", "#64748b", "#e87979"],
  dataLabels: { enabled: true },
  stroke: { width: 0 },
  legend: {
    position: "bottom",
    fontSize: "11px",
    labels: { colors: "#78809b" },
  },
  grid: { borderColor: "#edf0f7", strokeDashArray: 4 },
  labels: chartData.value.labels,
  plotOptions: {
    bar: { borderRadius: 3, columnWidth: "48%" },
    pie: { donut: { size: "58%" } },
  },
  fill: { opacity: 1 },
  tooltip: { theme: "light" },
}));

</script>

<template>
  <ChartPanel title="Completed Operations" subtitle="Completed versus pending job cards">
    <VueApexCharts
      width="100%"
      height="210"
      type="donut"
      :options="options"
      :series="chartData.value.series"
    />
  </ChartPanel>
</template>
