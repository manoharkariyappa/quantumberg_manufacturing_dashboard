function getFrappe() {
  return window.frappe;
}

export function call(method, args = {}) {
  const frappe = getFrappe();

  if (!frappe?.call) {
    return Promise.reject(
      new Error("Frappe API is not available. Open this page from Desk.")
    );
  }

  return new Promise((resolve, reject) => {
    frappe.call({
      method,
      args,
      type: "POST",
      callback: (response) => resolve(response?.message),
      error: (error) =>
        reject(new Error(error?.message || "Request failed")),
    });
  });
}

export function getList(doctype, options = {}) {
  return call("frappe.client.get_list", {
    doctype,
    ...options,
  });
}

export function openList(doctype, filters = null) {
  if (!doctype) {
    return;
  }

  if (getFrappe()?.set_route) {
    getFrappe().route_options =
      filters && Object.keys(filters).length ? filters : null;
    getFrappe().set_route("List", doctype);
    return;
  }

  window.location.href = `/app/${encodeURIComponent(
    String(doctype).toLowerCase().replace(/\s+/g, "-")
  )}`;
}
