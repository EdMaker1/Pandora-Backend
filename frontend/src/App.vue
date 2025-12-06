<template>
  <div class="min-h-screen bg-gray-100">
    <!-- Navbar (solo si está logueado) -->
    <nav v-if="isAuthenticated" class="bg-gradient-to-r from-primary to-secondary text-white shadow-lg">
      <div class="container mx-auto px-6 py-4">
        <div class="flex items-center justify-between">
          <div class="flex items-center space-x-4">
            <h1 class="text-2xl font-bold">📚 Librería Pandora</h1>
          </div>
          
          <!-- Menu según rol -->
          <div class="flex items-center space-x-6">
            <router-link to="/" class="hover:text-gray-200 transition">Inicio</router-link>
            
            <!-- ADMINISTRADOR y SOPORTE: Acceso completo -->
            <template v-if="['ADMINISTRADOR', 'SOPORTE'].includes(user?.rol)">
              <router-link to="/categorias" class="hover:text-gray-200 transition">Categorías</router-link>
              <router-link to="/productos" class="hover:text-gray-200 transition">Productos</router-link>
              <router-link to="/clientes" class="hover:text-gray-200 transition">Clientes</router-link>
              <router-link to="/ventas" class="hover:text-gray-200 transition">Ventas</router-link>
              <router-link to="/empleados" class="hover:text-gray-200 transition">Empleados</router-link>
              <router-link to="/pagos" class="hover:text-gray-200 transition">Pagos</router-link>
              <router-link to="/stock" class="hover:text-gray-200 transition">Stock</router-link>
              <router-link to="/reportes" class="hover:text-gray-200 transition">Reportes</router-link>
            </template>
            
            <!-- VENDEDOR: Ventas, productos, categorías y clientes -->
            <template v-else-if="user?.rol === 'VENDEDOR'">
              <router-link to="/categorias" class="hover:text-gray-200 transition">Categorías</router-link>
              <router-link to="/productos" class="hover:text-gray-200 transition">Productos</router-link>
              <router-link to="/clientes" class="hover:text-gray-200 transition">Clientes</router-link>
              <router-link to="/ventas" class="hover:text-gray-200 transition">Ventas</router-link>
            </template>
            
            <!-- CAJERO: Ventas, productos, categorías, clientes, reportes y pagos -->
            <template v-else-if="user?.rol === 'CAJERO'">
              <router-link to="/categorias" class="hover:text-gray-200 transition">Categorías</router-link>
              <router-link to="/productos" class="hover:text-gray-200 transition">Productos</router-link>
              <router-link to="/clientes" class="hover:text-gray-200 transition">Clientes</router-link>
              <router-link to="/ventas" class="hover:text-gray-200 transition">Ventas</router-link>
              <router-link to="/pagos" class="hover:text-gray-200 transition">Pagos</router-link>
              <router-link to="/reportes" class="hover:text-gray-200 transition">Reportes</router-link>
            </template>
            
            <!-- ALMACEN: Solo productos, categorías y stock -->
            <template v-else-if="user?.rol === 'ALMACEN'">
              <router-link to="/categorias" class="hover:text-gray-200 transition">Categorías</router-link>
              <router-link to="/productos" class="hover:text-gray-200 transition">Productos</router-link>
              <router-link to="/stock" class="hover:text-gray-200 transition">Stock</router-link>
            </template>

            <!-- Usuario y Logout -->
            <div class="relative group">
              <button class="flex items-center space-x-2 hover:text-gray-200 transition">
                <img v-if="user?.picture" :src="user.picture" class="w-8 h-8 rounded-full" :alt="user.nombre_completo" />
                <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clip-rule="evenodd"></path>
                </svg>
                <span>{{ user?.nombre_completo || user?.username }}</span>
                <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                  <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"></path>
                </svg>
              </button>
              
              <!-- Dropdown -->
              <div class="absolute right-0 mt-2 w-48 bg-white rounded-lg shadow-lg py-2 hidden group-hover:block z-50">
                <div class="px-4 py-2 border-b border-gray-200">
                  <p class="text-sm font-semibold text-gray-700">{{ user?.username }}</p>
                  <p class="text-xs text-gray-500">{{ user?.rol }}</p>
                  <p v-if="user?.login_method === 'google'" class="text-xs text-blue-600 mt-1">🔐 Login con Google</p>
                </div>
                <button @click="handleLogout" class="w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-red-50 flex items-center space-x-2">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fill-rule="evenodd" d="M3 3a1 1 0 00-1 1v12a1 1 0 102 0V4a1 1 0 00-1-1zm10.293 9.293a1 1 0 001.414 1.414l3-3a1 1 0 000-1.414l-3-3a1 1 0 10-1.414 1.414L14.586 9H7a1 1 0 100 2h7.586l-1.293 1.293z" clip-rule="evenodd"></path>
                  </svg>
                  <span>Cerrar Sesión</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </nav>

    <!-- Contenido principal -->
    <main :class="isAuthenticated ? 'container mx-auto px-6 py-8' : ''">
      <router-view></router-view>
    </main>

    <!-- Footer (solo si está logueado) -->
    <footer v-if="isAuthenticated" class="bg-gray-800 text-white text-center py-4 mt-12">
      <p>&copy; 2025 Librería Pandora - Sistema de Gestión</p>
    </footer>
  </div>
</template>

<script>
import api from './services/api'

export default {
  name: 'App',
  data() {
    return {
      user: null,
      loading: true
    }
  },
  computed: {
    isAuthenticated() {
      return !!this.user
    }
  },
  async mounted() {
    await this.checkAuth()
  },
  methods: {
    async checkAuth() {
      try {
        // Primero intentar obtener usuario del servidor (sesión)
        const response = await api.auth.me()
        this.user = response.data
        // Sincronizar con localStorage para compatibilidad
        localStorage.setItem('user', JSON.stringify(response.data))
      } catch (error) {
        // Si falla, intentar obtener de localStorage (login tradicional)
        const userData = localStorage.getItem('user')
        if (userData) {
          this.user = JSON.parse(userData)
        } else {
          this.user = null
        }
      } finally {
        this.loading = false
      }
    },
    async handleLogout() {
      try {
        await api.auth.logout()
        localStorage.removeItem('user')
        this.user = null
        this.$router.push('/login')
      } catch (error) {
        console.error('Error al cerrar sesión:', error)
        // Limpiar de todas formas
        localStorage.removeItem('user')
        this.user = null
        this.$router.push('/login')
      }
    }
  },
  watch: {
    async '$route'() {
      if (!this.user) {
        await this.checkAuth()
      }
    }
  }
}
</script>