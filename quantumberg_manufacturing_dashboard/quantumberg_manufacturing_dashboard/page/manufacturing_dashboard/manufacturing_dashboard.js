frappe.pages["manufacturing-dashboard"].on_page_load = function (wrapper) {
  const page = frappe.ui.make_app_page({
    parent: wrapper,
    title: "Manufacturing Dashboard",
    single_column: true,
  });

  page.main.html(`
    <div
      id="quantumberg-manufacturing-dashboard-root"
      style="width:100%; min-height:80vh;"
    >
      <div style="padding:24px;color:#64748b;">
        Loading Manufacturing Dashboard...
      </div>
    </div>
  `);

  const root = page.main.find(
    "#quantumberg-manufacturing-dashboard-root"
  )[0];

  const cssPath =
    "/assets/quantumberg_manufacturing_dashboard/dashboard/index.css";

  const jsPath =
    "/assets/quantumberg_manufacturing_dashboard/dashboard/index.js";

  function loadCSS() {
    let link = document.querySelector(
      'link[data-quantumberg-manufacturing-dashboard="css"]'
    );

    if (!link) {
      link = document.createElement("link");
      link.rel = "stylesheet";
      link.dataset.quantumbergManufacturingDashboard = "css";
      document.head.appendChild(link);
    }

    link.href = cssPath;

    return new Promise((resolve, reject) => {
      if (link.dataset.loaded === "true" && link.href === cssPath) {
        resolve();
        return;
      }

      link.onload = () => {
        link.dataset.loaded = "true";
        resolve();
      };

      link.onerror = () => {
        reject(new Error("Failed to load Manufacturing Dashboard CSS"));
      };
    });
  }

  function loadJS() {
    if (window.QuantumbergManufacturingDashboard) {
      return Promise.resolve();
    }

    return new Promise((resolve, reject) => {
      let script = document.querySelector(
        'script[data-quantumberg-manufacturing-dashboard="js"]'
      );

      if (script) {
        if (script.dataset.loaded === "true") {
          resolve();
          return;
        }

        script.addEventListener("load", resolve, { once: true });
        script.addEventListener(
          "error",
          () => reject(
            new Error("Failed to load Manufacturing Dashboard JavaScript")
          ),
          { once: true }
        );

        return;
      }

      script = document.createElement("script");
      script.src = jsPath;
      script.dataset.quantumbergManufacturingDashboard = "js";

      script.onload = () => {
        script.dataset.loaded = "true";
        resolve();
      };

      script.onerror = () => {
        reject(
          new Error("Failed to load Manufacturing Dashboard JavaScript")
        );
      };

      document.body.appendChild(script);
    });
  }

  async function initializeDashboard() {
    try {
      await loadCSS();
      await loadJS();

      const dashboard = window.QuantumbergManufacturingDashboard;

      if (!dashboard || typeof dashboard.mount !== "function") {
        throw new Error(
          "Vue mount function is missing. Check frontend/src/main.js."
        );
      }

      dashboard.mount(root);
    } catch (error) {
      console.error("Manufacturing Dashboard initialization failed:", error);

      root.innerHTML = `
        <div style="
          margin:20px;
          padding:20px;
          background:#fff1f2;
          color:#be123c;
          border-radius:8px;
        ">
          <h3>Unable to load Manufacturing Dashboard</h3>
          <p>${frappe.utils.escape_html(error.message || String(error))}</p>
          <p>Check the browser Console for details.</p>
        </div>
      `;
    }
  }

  initializeDashboard();
};