import { createApp } from 'vue'
import './style.css'
import App from './App.vue'

let app = null

window.QuantumbergManufacturingDashboard = {
  mount(element) {
    if (!element) {
      throw new Error('Manufacturing Dashboard root element not found')
    }

    if (app) {
      app.unmount()
      app = null
    }

    app = createApp(App)
    app.mount(element)
  },

  unmount() {
    if (app) {
      app.unmount()
      app = null
    }
  },
}

// Keep the dashboard working with the standalone Vite development page.
const devRoot = document.getElementById('app')

if (devRoot) {
  window.QuantumbergManufacturingDashboard.mount(devRoot)
}