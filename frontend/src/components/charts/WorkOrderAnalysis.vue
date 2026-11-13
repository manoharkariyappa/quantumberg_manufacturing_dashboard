<script setup>
import { computed } from "vue";
import VueApexCharts from "vue3-apexcharts";
import ChartPanel from "./ChartPanel.vue";
import { workOrderAnalysis as demoWorkOrderAnalysis } from "../../data/manufacturingData.js";

const props = defineProps({
  data: { type: Object, default: null },
});

const source = computed(() => props.data || demoWorkOrderAnalysis);

const series = computed(() => source.value.values || source.value.series || []);

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
  stroke: { curve: "smooth", width: 0 },
  legend: {
    position: "bottom",
    fontSize: "11px",
    labels: { colors: "#78809b" },
  },
  grid: { borderColor: "#edf0f7", strokeDashArray: 4 },
  xaxis: {
    categories: source.value.labels,
    labels: { style: { fontSize: "10px", colors: "#78809b" } },
  },
  yaxis: {
    labels: { style: { fontSize: "10px", colors: "#78809b" } },
  },
  labels: source.value.labels,
  plotOptions: {
    bar: { borderRadius: 3, columnWidth: "48%" },
    pie: { donut: { size: "58%" } },
  },
  fill: { opacity: 1 },
  tooltip: { theme: "light" },
}));

</script>

<template>
  <ChartPanel title="Work Order Analysis" subtitle="Distribution by work order status">
    <VueApexCharts
      width="100%"
      height="210"
      type="donut"
      :options="options"
      :series="series"
    />
  </ChartPanel>
</template>
