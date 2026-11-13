<script setup>
import { computed } from "vue";
import VueApexCharts from "vue3-apexcharts";
import ChartPanel from "./ChartPanel.vue";
import { workOrderQuantity as demoWorkOrderQuantity } from "../../data/manufacturingData.js";

const props = defineProps({
  data: { type: Object, default: null },
});

const chartData = computed(() => {
  const data = props.data;

  if (!data) {
    return demoWorkOrderQuantity;
  }

  return {
    categories: data.labels || [],
    series: [
      { name: "Planned Qty", data: data.planned || [] },
      { name: "Produced Qty", data: data.produced || [] },
    ],
  };
});

const options = computed(() => ({
  chart: {
    type: "bar",
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
  <ChartPanel title="Work Order Quantity" subtitle="Pending versus completed quantity">
    <VueApexCharts
      width="100%"
      height="210"
      type="bar"
      :options="options"
      :series="chartData.value.series"
    />
  </ChartPanel>
</template>
