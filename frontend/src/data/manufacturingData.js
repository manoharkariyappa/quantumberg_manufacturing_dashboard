export const summaryCards = [
  {
    title: "Open Work Orders",
    value: 24,
    valueKey: "open_work_orders",
    description: "View Open Work Orders",
    color: "purple",
    list: {
      doctype: "Work Order",
      dateField: "planned_start_date",
      filters: {
        docstatus: 1,
        status: [
          "in",
          [
            "Not Started",
            "In Process",
            "Stock Reserved",
            "Stock Partially Reserved",
          ],
        ],
      },
    },
  },
  {
    title: "WIP Work Orders",
    value: 12,
    valueKey: "wip_work_orders",
    description: "View Work Orders in Progress",
    color: "blue",
    list: {
      doctype: "Work Order",
      dateField: "planned_start_date",
      filters: { docstatus: 1, status: "In Process" },
    },
  },
  {
    title: "Manufactured Items Value",
    value: "₹ 2,45,680.00",
    valueKey: "manufactured_items_value",
    format: "currency",
    description: "View Completed Work Orders",
    color: "green",
    list: {
      doctype: "Work Order",
      dateField: "planned_start_date",
      filters: { docstatus: 1, status: "Completed" },
    },
  },
  {
    title: "Items in Production",
    value: 18,
    valueKey: "items_in_production",
    description: "Active production job cards",
    color: "orange",
    list: {
      doctype: "Job Card",
      dateField: "posting_date",
      filters: { docstatus: ["<", 2], status: "Work In Progress" },
    },
  },
];

export const workOrderAnalysis = {
  labels: ["Not Started", "In Process", "Stock Reserved", "Stock Partially Reserved", "Completed", "Stopped", "Closed", "Cancelled"],
  series: [8, 12, 5, 3, 28, 2, 6, 1],
};

export const jobCardAnalysis = {
  categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  series: [
    { name: "Completed", data: [12, 15, 18, 22, 19, 25, 28, 31, 29, 35, 38, 42] },
    { name: "Pending", data: [8, 10, 7, 12, 9, 11, 8, 7, 10, 6, 8, 5] },
  ],
};

export const producedQuantity = {
  categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  series: [{ name: "Produced Quantity", data: [22, 27, 31, 49, 43, 51, 46, 61, 68, 79, 74, 88] }],
};

export const completedOperation = {
  categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  series: [{ name: "Completed Quantity", data: [20, 34, 42, 36, 51, 44, 57, 48, 61, 65, 79, 91] }],
};

export const workOrderQuantity = {
  categories: ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"],
  series: [
    { name: "Pending Qty", data: [45, 55, 60, 70, 75, 85, 90, 100, 115, 130, 145, 160] },
    { name: "Completed Qty", data: [25, 35, 40, 48, 55, 60, 70, 80, 92, 100, 115, 125] },
  ],
};

export const pendingWorkOrder = {
  labels: ["< 30 Days", "30 - 60 Days", "60 - 90 Days", "> 90 Days"],
  series: [8, 5, 3, 2],
};

export const qualityInspection = {
  labels: ["Accepted", "Rejected"],
  series: [92, 8],
};

export const downtimeAnalysis = {
  categories: ["1 Jul", "5 Jul", "10 Jul", "15 Jul", "20 Jul", "25 Jul", "30 Jul"],
  series: [{ name: "Downtime (minutes)", data: [25, 38, 45, 32, 41, 43, 55] }],
};

export const manufacturingReports = [
  { title: "Work Order Summary", description: "Detailed work order report", count: 83 },
  { title: "Open Work Orders", description: "List of open work orders", count: 24 },
  { title: "Completed Work Orders", description: "List of completed work orders", count: 28 },
  { title: "Work Orders in Progress", description: "Work orders in production", count: 12 },
  { title: "Job Card Summary", description: "Job card analysis", count: 46 },
  { title: "Production Analytics", description: "Production performance", count: 12 },
  { title: "Production Plan Summary", description: "Production plan report", count: 7 },
  { title: "Production Planning Report", description: "Detailed planning report", count: 18 },
  { title: "Quality Inspection Summary", description: "Quality inspection results", count: 100 },
  { title: "Downtime Analysis", description: "Workstation downtime", count: 15 },
];
