import { call } from "./api.js";

const API = "quantumberg_manufacturing_dashboard.api";

function unwrap(response) {
  if (response && typeof response === "object" && "data" in response) {
    return response.data;
  }

  return response;
}

export async function fetchDashboardData(params = {}) {
  const [
    summary,
    workOrderAnalysis,
    jobCardAnalysis,
    producedQuantity,
    completedOperation,
    workOrderQuantity,
    pendingWorkOrder,
    qualityInspection,
    downtimeAnalysis,
    reports,
  ] = await Promise.all([
    call(`${API}.get_dashboard_summary`, params),
    call(`${API}.get_work_order_analysis`, params),
    call(`${API}.get_job_card_analysis`, params),
    call(`${API}.get_produced_quantity`, params),
    call(`${API}.get_completed_operations`, params),
    call(`${API}.get_work_order_quantity`, params),
    call(`${API}.get_pending_work_orders`, params),
    call(`${API}.get_quality_inspection_analysis`, params),
    call(`${API}.get_downtime_analysis`, params),
    call(`${API}.get_manufacturing_reports`, params),
  ]);

  return {
    summary: unwrap(summary),
    workOrderAnalysis: unwrap(workOrderAnalysis),
    jobCardAnalysis: unwrap(jobCardAnalysis),
    producedQuantity: unwrap(producedQuantity),
    completedOperation: unwrap(completedOperation),
    workOrderQuantity: unwrap(workOrderQuantity),
    pendingWorkOrder: unwrap(pendingWorkOrder),
    qualityInspection: unwrap(qualityInspection),
    downtimeAnalysis: unwrap(downtimeAnalysis),
    reports: unwrap(reports),
  };
}
