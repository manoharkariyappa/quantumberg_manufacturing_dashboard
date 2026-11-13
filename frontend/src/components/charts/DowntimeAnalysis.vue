<script setup>
import { computed } from "vue";
import VueApexCharts from "vue3-apexcharts";
import ChartPanel from "./ChartPanel.vue";
import { downtimeAnalysis as demoDowntimeAnalysis } from "../../data/manufacturingData.js";

const props = defineProps({
  data: { type: Object, default: null },
});

const chartData = computed(() => {
  const data = props.data;

  if (!data) {
    return demoDowntimeAnalysis;
  }

  return {
    categories: data.labels || [],
    series: [
      { name: "Downtime (minutes)", data: data.values || [] },
    ],
  };
});

const options = computed(() => ({
  chart: {
    type: "line",
    height: 210,
    toolbar: { show: false },
    fontFamily: "var(--font-stack, inherit)",
    animations: { enabled: true, speed: 350 },
  },
  colors: ["#493b91", "#3987f5", "#20bf88", "#c43f9d", "#ffad19", "#8b83c9", "#64748b", "#e87979"],
  dataLabels: { enabled: false },
  stroke: { curve: "smooth", width: 3 },
  legend: {
    position: "bottom",
    fontSize: "11px",
    labels: { colors: "#78809b" },
  },
  grid: { borderColor: "#edf0f7", strokeDashArray: 4 },
  xaxis: {
    categories: chartData.value.categories,
    labels: { style: { fontSize: "10px", colors: "#78809b" } },
  },
  yaxis: {
    labels: { style: { fontSize: "10px", colors: "#78809b" } },
  },
  labels: undefined,
  plotOptions: {
    bar: { borderRadius: 3, columnWidth: "48%" },
    pie: { donut: { size: "58%" } },
  },
  fill: { opacity: 1 },
  tooltip: { theme: "light" },
}));

</script>

<template>
  <ChartPanel title="Downtime Analysis" subtitle="Machine downtime in minutes">
    <VueApexCharts
      width="100%"
      height="210"
      type="line"
      :options="options"
      :series="chartData.value.series"
    />
  </ChartPanel>
</template>
