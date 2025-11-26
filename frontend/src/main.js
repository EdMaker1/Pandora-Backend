import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Importar vistas
import Home from './views/Home.vue'
import Categorias from './views/Categorias.vue'
import Productos from './views/Productos.vue'
import Clientes from './views/Clientes.vue'
import Ventas from './views/Ventas.vue'

const routes = [
  { path: '/', component: Home },
  { path: '/categorias', component: Categorias },
  { path: '/productos', component: Productos },
  { path: '/clientes', component: Clientes },
  { path: '/ventas', component: Ventas }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

const app = createApp(App)
app.use(router)
app.mount('#app')