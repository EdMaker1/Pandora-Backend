import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import App from './App.vue'

// Importar vistas
import Login from './views/Login.vue'
import Home from './views/Home.vue'
import Categorias from './views/Categorias.vue'
import Productos from './views/Productos.vue'
import Clientes from './views/Clientes.vue'
import Ventas from './views/Ventas.vue'
import Empleados from './views/Empleados.vue'
import Pagos from './views/Pagos.vue'
import Stock from './views/Stock.vue'
import Reportes from './views/Reportes.vue'

// Función helper para verificar autenticación
function isAuthenticated() {
  return !!localStorage.getItem('user')
}

// Función helper para obtener el rol del usuario
function getUserRole() {
  const user = localStorage.getItem('user')
  return user ? JSON.parse(user).rol : null
}

// Función helper para verificar si el usuario tiene acceso
function hasAccess(allowedRoles) {
  const role = getUserRole()
  return allowedRoles.includes(role)
}

const routes = [
  {
    path: '/login',
    component: Login,
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: Home,
    meta: { requiresAuth: true }
  },
  {
    path: '/categorias',
    component: Categorias,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN']
    }
  },
  {
    path: '/productos',
    component: Productos,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO', 'ALMACEN']
    }
  },
  {
    path: '/clientes',
    component: Clientes,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO']
    }
  },
  {
    path: '/ventas',
    component: Ventas,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'VENDEDOR', 'CAJERO']
    }
  },
  {
    path: '/empleados',
    component: Empleados,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE']
    }
  },
  {
    path: '/pagos',
    component: Pagos,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'CAJERO']
    }
  },
  {
    path: '/stock',
    component: Stock,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'ALMACEN']
    }
  },
  {
    path: '/reportes',
    component: Reportes,
    meta: { 
      requiresAuth: true,
      allowedRoles: ['ADMINISTRADOR', 'SOPORTE', 'CAJERO']
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Guard global de navegación
router.beforeEach((to, from, next) => {
  const requiresAuth = to.meta.requiresAuth
  const allowedRoles = to.meta.allowedRoles

  // Si la ruta requiere autenticación
  if (requiresAuth && !isAuthenticated()) {
    next('/login')
    return
  }

  // Si está autenticado y va a login, redirigir a home
  if (to.path === '/login' && isAuthenticated()) {
    next('/')
    return
  }

  // Verificar permisos de rol
  if (requiresAuth && allowedRoles && !hasAccess(allowedRoles)) {
    alert('No tienes permisos para acceder a esta sección')
    next('/')
    return
  }

  next()
})

const app = createApp(App)
app.use(router)
app.mount('#app')